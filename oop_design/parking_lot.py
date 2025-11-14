"""
Parking Lot System - OOP Design Example

Demonstrates system design with multiple interacting classes.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional, List


class VehicleType(Enum):
    """Types of vehicles."""
    MOTORCYCLE = 1
    CAR = 2
    TRUCK = 3


class ParkingSpotType(Enum):
    """Types of parking spots."""
    COMPACT = 1
    REGULAR = 2
    LARGE = 3


class Vehicle(ABC):
    """Abstract vehicle class."""

    def __init__(self, license_plate: str):
        self._license_plate = license_plate
        self._vehicle_type: VehicleType

    @property
    def license_plate(self) -> str:
        return self._license_plate

    @property
    @abstractmethod
    def vehicle_type(self) -> VehicleType:
        pass


class Motorcycle(Vehicle):
    """Motorcycle vehicle."""

    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.MOTORCYCLE


class Car(Vehicle):
    """Car vehicle."""

    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.CAR


class Truck(Vehicle):
    """Truck vehicle."""

    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.TRUCK


class ParkingSpot:
    """Represents a parking spot."""

    def __init__(self, spot_id: int, spot_type: ParkingSpotType):
        self._spot_id = spot_id
        self._spot_type = spot_type
        self._vehicle: Optional[Vehicle] = None

    @property
    def spot_id(self) -> int:
        return self._spot_id

    @property
    def spot_type(self) -> ParkingSpotType:
        return self._spot_type

    def is_available(self) -> bool:
        """Check if spot is available."""
        return self._vehicle is None

    def can_fit_vehicle(self, vehicle: Vehicle) -> bool:
        """Check if vehicle can fit in this spot."""
        if vehicle.vehicle_type == VehicleType.MOTORCYCLE:
            return True
        elif vehicle.vehicle_type == VehicleType.CAR:
            return self._spot_type in [ParkingSpotType.REGULAR, ParkingSpotType.LARGE]
        elif vehicle.vehicle_type == VehicleType.TRUCK:
            return self._spot_type == ParkingSpotType.LARGE
        return False

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        """Park a vehicle in this spot."""
        if self.is_available() and self.can_fit_vehicle(vehicle):
            self._vehicle = vehicle
            return True
        return False

    def remove_vehicle(self) -> Optional[Vehicle]:
        """Remove vehicle from spot."""
        vehicle = self._vehicle
        self._vehicle = None
        return vehicle


class ParkingTicket:
    """Parking ticket issued when vehicle enters."""

    _ticket_counter = 0

    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        ParkingTicket._ticket_counter += 1
        self._ticket_id = ParkingTicket._ticket_counter
        self._vehicle = vehicle
        self._spot = spot
        self._issued_at = datetime.now()
        self._paid_at: Optional[datetime] = None
        self._fee = 0.0

    @property
    def ticket_id(self) -> int:
        return self._ticket_id

    @property
    def spot(self) -> ParkingSpot:
        return self._spot

    @property
    def vehicle(self) -> Vehicle:
        return self._vehicle

    def calculate_fee(self, hourly_rate: float = 5.0) -> float:
        """Calculate parking fee."""
        duration = datetime.now() - self._issued_at
        hours = max(1, duration.total_seconds() / 3600)
        self._fee = hours * hourly_rate
        return self._fee

    def pay(self) -> None:
        """Mark ticket as paid."""
        self._paid_at = datetime.now()

    def is_paid(self) -> bool:
        """Check if ticket is paid."""
        return self._paid_at is not None


class ParkingLevel:
    """Represents a level in the parking lot."""

    def __init__(self, level_number: int):
        self._level_number = level_number
        self._spots: List[ParkingSpot] = []

    def add_spot(self, spot: ParkingSpot) -> None:
        """Add a parking spot to this level."""
        self._spots.append(spot)

    def find_available_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Find an available spot for the vehicle."""
        for spot in self._spots:
            if spot.is_available() and spot.can_fit_vehicle(vehicle):
                return spot
        return None

    def get_available_count(self) -> int:
        """Get count of available spots."""
        return sum(1 for spot in self._spots if spot.is_available())


class ParkingLot:
    """Main parking lot system."""

    def __init__(self, name: str):
        self._name = name
        self._levels: List[ParkingLevel] = []
        self._tickets: dict[int, ParkingTicket] = {}

    def add_level(self, level: ParkingLevel) -> None:
        """Add a level to the parking lot."""
        self._levels.append(level)

    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingTicket]:
        """Park a vehicle and issue a ticket."""
        for level in self._levels:
            spot = level.find_available_spot(vehicle)
            if spot:
                if spot.park_vehicle(vehicle):
                    ticket = ParkingTicket(vehicle, spot)
                    self._tickets[ticket.ticket_id] = ticket
                    return ticket
        return None

    def exit_vehicle(self, ticket_id: int) -> Optional[float]:
        """Process vehicle exit and return fee."""
        ticket = self._tickets.get(ticket_id)
        if ticket:
            if not ticket.is_paid():
                return None  # Must pay first

            spot = ticket.spot
            spot.remove_vehicle()
            del self._tickets[ticket_id]
            return ticket._fee
        return None

    def pay_ticket(self, ticket_id: int) -> Optional[float]:
        """Pay for a parking ticket."""
        ticket = self._tickets.get(ticket_id)
        if ticket:
            fee = ticket.calculate_fee()
            ticket.pay()
            return fee
        return None

    def get_available_spots_count(self) -> int:
        """Get total available spots."""
        return sum(level.get_available_count() for level in self._levels)
