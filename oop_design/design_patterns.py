"""
Common Design Patterns Implementation
"""
from abc import ABC, abstractmethod
from typing import List, Optional


# Singleton Pattern
class Singleton:
    """
    Singleton pattern ensures a class has only one instance.

    Example:
        >>> s1 = Singleton()
        >>> s2 = Singleton()
        >>> s1 is s2
        True
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# Factory Pattern
class Animal(ABC):
    """Abstract Animal class."""

    @abstractmethod
    def speak(self) -> str:
        pass


class Dog(Animal):
    """Dog implementation."""

    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    """Cat implementation."""

    def speak(self) -> str:
        return "Meow!"


class AnimalFactory:
    """
    Factory pattern for creating animals.

    Example:
        >>> factory = AnimalFactory()
        >>> dog = factory.create_animal("dog")
        >>> dog.speak()
        'Woof!'
    """

    @staticmethod
    def create_animal(animal_type: str) -> Optional[Animal]:
        """Create an animal based on type."""
        if animal_type.lower() == "dog":
            return Dog()
        elif animal_type.lower() == "cat":
            return Cat()
        return None


# Observer Pattern
class Subject:
    """Subject in Observer pattern."""

    def __init__(self):
        self._observers: List['Observer'] = []
        self._state: Optional[str] = None

    def attach(self, observer: 'Observer') -> None:
        """Attach an observer."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: 'Observer') -> None:
        """Detach an observer."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(self)

    def set_state(self, state: str) -> None:
        """Set state and notify observers."""
        self._state = state
        self.notify()

    def get_state(self) -> Optional[str]:
        """Get current state."""
        return self._state


class Observer(ABC):
    """Abstract Observer."""

    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass


class ConcreteObserver(Observer):
    """Concrete Observer implementation."""

    def __init__(self, name: str):
        self.name = name

    def update(self, subject: Subject) -> None:
        """Update based on subject state."""
        print(f"{self.name} received update: {subject.get_state()}")


# Strategy Pattern
class SortStrategy(ABC):
    """Abstract sorting strategy."""

    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass


class BubbleSortStrategy(SortStrategy):
    """Bubble sort strategy."""

    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class QuickSortStrategy(SortStrategy):
    """Quick sort strategy."""

    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class Sorter:
    """
    Context class for Strategy pattern.

    Example:
        >>> sorter = Sorter(QuickSortStrategy())
        >>> sorter.sort([3, 1, 4, 1, 5, 9, 2, 6])
        [1, 1, 2, 3, 4, 5, 6, 9]
    """

    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        """Change sorting strategy."""
        self._strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        """Sort using current strategy."""
        return self._strategy.sort(data)


# Decorator Pattern
class Component(ABC):
    """Abstract component."""

    @abstractmethod
    def operation(self) -> str:
        pass


class ConcreteComponent(Component):
    """Concrete component."""

    def operation(self) -> str:
        return "ConcreteComponent"


class Decorator(Component):
    """Base decorator."""

    def __init__(self, component: Component):
        self._component = component

    def operation(self) -> str:
        return self._component.operation()


class ConcreteDecoratorA(Decorator):
    """Concrete decorator A."""

    def operation(self) -> str:
        return f"DecoratorA({self._component.operation()})"


class ConcreteDecoratorB(Decorator):
    """Concrete decorator B."""

    def operation(self) -> str:
        return f"DecoratorB({self._component.operation()})"
