"""
Problem: Inventory Management System

Design an inventory management system that tracks products,
stock levels, and handles orders.

Requirements:
1. Add/remove products
2. Update stock levels
3. Process orders (check availability, update stock)
4. Track low stock items
5. Generate inventory reports
6. Handle concurrent operations safely

Example:
    inventory = InventorySystem()
    inventory.add_product("SKU001", "Laptop", 10, 999.99)
    inventory.process_order("SKU001", 3)  # True (stock: 10 -> 7)
    inventory.get_low_stock_items(threshold=5)  # []

Difficulty: Medium
Time: 35-45 minutes
Focus: System design, data structures, business logic
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from threading import Lock
from enum import Enum


class OrderStatus(Enum):
    """Order status types."""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    INSUFFICIENT_STOCK = "insufficient_stock"


@dataclass
class Product:
    """Product in inventory."""
    sku: str
    name: str
    quantity: int
    price: float
    reorder_point: int = 10
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Order:
    """Order record."""
    order_id: str
    sku: str
    quantity: int
    status: OrderStatus
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class InventorySystem:
    """
    Thread-safe inventory management system.

    Manages products, stock levels, and order processing.
    """

    def __init__(self):
        """Initialize inventory system."""
        self.products: Dict[str, Product] = {}
        self.orders: List[Order] = []
        self.order_counter = 0
        self.lock = Lock()

    def add_product(
        self,
        sku: str,
        name: str,
        quantity: int,
        price: float,
        reorder_point: int = 10
    ) -> bool:
        """
        Add new product to inventory.

        Args:
            sku: Stock keeping unit (unique identifier)
            name: Product name
            quantity: Initial stock quantity
            price: Product price
            reorder_point: Minimum stock level before reorder

        Returns:
            True if added, False if SKU already exists
        """
        with self.lock:
            if sku in self.products:
                return False

            self.products[sku] = Product(
                sku=sku,
                name=name,
                quantity=quantity,
                price=price,
                reorder_point=reorder_point
            )
            return True

    def remove_product(self, sku: str) -> bool:
        """
        Remove product from inventory.

        Args:
            sku: Product SKU

        Returns:
            True if removed, False if not found
        """
        with self.lock:
            if sku in self.products:
                del self.products[sku]
                return True
            return False

    def update_stock(self, sku: str, quantity: int) -> bool:
        """
        Update stock quantity for a product.

        Args:
            sku: Product SKU
            quantity: New quantity (not delta)

        Returns:
            True if updated, False if product not found
        """
        with self.lock:
            if sku not in self.products:
                return False

            self.products[sku].quantity = max(0, quantity)
            return True

    def add_stock(self, sku: str, quantity: int) -> bool:
        """
        Add to existing stock.

        Args:
            sku: Product SKU
            quantity: Quantity to add

        Returns:
            True if updated, False if product not found
        """
        with self.lock:
            if sku not in self.products:
                return False

            self.products[sku].quantity += quantity
            return True

    def get_product(self, sku: str) -> Optional[Product]:
        """Get product by SKU."""
        return self.products.get(sku)

    def get_stock_level(self, sku: str) -> Optional[int]:
        """Get current stock level for product."""
        product = self.get_product(sku)
        return product.quantity if product else None

    def process_order(self, sku: str, quantity: int) -> Tuple[bool, str]:
        """
        Process an order.

        Args:
            sku: Product SKU
            quantity: Order quantity

        Returns:
            Tuple of (success, order_id or error message)
        """
        with self.lock:
            # Check if product exists
            if sku not in self.products:
                order_id = self._create_order(sku, quantity, OrderStatus.CANCELLED)
                return False, f"Product {sku} not found"

            product = self.products[sku]

            # Check stock availability
            if product.quantity < quantity:
                order_id = self._create_order(sku, quantity, OrderStatus.INSUFFICIENT_STOCK)
                return False, f"Insufficient stock. Available: {product.quantity}, Requested: {quantity}"

            # Process order
            product.quantity -= quantity
            order_id = self._create_order(sku, quantity, OrderStatus.COMPLETED)

            return True, order_id

    def _create_order(self, sku: str, quantity: int, status: OrderStatus) -> str:
        """Create order record (must be called within lock)."""
        self.order_counter += 1
        order_id = f"ORD{self.order_counter:06d}"

        order = Order(
            order_id=order_id,
            sku=sku,
            quantity=quantity,
            status=status
        )

        self.orders.append(order)
        return order_id

    def get_low_stock_items(self, threshold: Optional[int] = None) -> List[Product]:
        """
        Get products with low stock.

        Args:
            threshold: Stock threshold (uses reorder_point if not specified)

        Returns:
            List of products below threshold
        """
        low_stock = []

        for product in self.products.values():
            limit = threshold if threshold is not None else product.reorder_point

            if product.quantity <= limit:
                low_stock.append(product)

        return sorted(low_stock, key=lambda p: p.quantity)

    def get_out_of_stock_items(self) -> List[Product]:
        """Get products with zero stock."""
        return [p for p in self.products.values() if p.quantity == 0]

    def get_inventory_value(self) -> float:
        """Calculate total inventory value."""
        return sum(
            product.quantity * product.price
            for product in self.products.values()
        )

    def get_product_value(self, sku: str) -> Optional[float]:
        """Get value of specific product's stock."""
        product = self.get_product(sku)
        return product.quantity * product.price if product else None

    def get_order_history(self, sku: Optional[str] = None) -> List[Order]:
        """
        Get order history.

        Args:
            sku: Filter by product SKU (optional)

        Returns:
            List of orders
        """
        if sku:
            return [order for order in self.orders if order.sku == sku]
        return list(self.orders)

    def get_sales_report(self) -> Dict[str, Dict]:
        """
        Generate sales report.

        Returns:
            Dictionary with sales statistics per product
        """
        report = {}

        for product in self.products.values():
            sku = product.sku

            # Get completed orders for this product
            completed_orders = [
                order for order in self.orders
                if order.sku == sku and order.status == OrderStatus.COMPLETED
            ]

            total_sold = sum(order.quantity for order in completed_orders)
            revenue = total_sold * product.price

            report[sku] = {
                'name': product.name,
                'total_sold': total_sold,
                'revenue': revenue,
                'current_stock': product.quantity,
                'order_count': len(completed_orders)
            }

        return report

    def __repr__(self) -> str:
        """String representation."""
        return f"InventorySystem({len(self.products)} products, {len(self.orders)} orders)"


# Test cases
if __name__ == '__main__':
    print("Testing Inventory Management System...\n")

    inventory = InventorySystem()

    # Test 1: Add products
    print("Test 1: Adding Products")
    inventory.add_product("LAP001", "Gaming Laptop", 15, 1299.99, reorder_point=5)
    inventory.add_product("MOU001", "Wireless Mouse", 50, 29.99, reorder_point=10)
    inventory.add_product("KEY001", "Mechanical Keyboard", 30, 89.99, reorder_point=8)

    print(f"Added 3 products")
    print(f"Inventory: {inventory}\n")

    # Test 2: Check stock levels
    print("Test 2: Stock Levels")
    for sku in ["LAP001", "MOU001", "KEY001"]:
        product = inventory.get_product(sku)
        print(f"{product.name}: {product.quantity} units @ ${product.price}")
    print()

    # Test 3: Process orders
    print("Test 3: Processing Orders")
    success, order_id = inventory.process_order("LAP001", 3)
    print(f"Order 3 laptops: {'Success' if success else 'Failed'} - {order_id}")

    success, order_id = inventory.process_order("MOU001", 10)
    print(f"Order 10 mice: {'Success' if success else 'Failed'} - {order_id}")

    # Check updated stock
    print(f"Laptop stock after order: {inventory.get_stock_level('LAP001')}")
    print(f"Mouse stock after order: {inventory.get_stock_level('MOU001')}\n")

    # Test 4: Insufficient stock
    print("Test 4: Insufficient Stock")
    success, message = inventory.process_order("LAP001", 100)
    print(f"Order 100 laptops: {message}\n")

    # Test 5: Low stock items
    print("Test 5: Low Stock Items")
    # Add more orders to trigger low stock
    inventory.process_order("LAP001", 10)

    low_stock = inventory.get_low_stock_items()
    print("Low stock items:")
    for product in low_stock:
        print(f"  {product.name}: {product.quantity} (reorder at {product.reorder_point})")
    print()

    # Test 6: Inventory value
    print("Test 6: Inventory Value")
    total_value = inventory.get_inventory_value()
    print(f"Total inventory value: ${total_value:,.2f}")

    for sku in ["LAP001", "MOU001", "KEY001"]:
        value = inventory.get_product_value(sku)
        product = inventory.get_product(sku)
        print(f"  {product.name}: ${value:,.2f}")
    print()

    # Test 7: Sales report
    print("Test 7: Sales Report")
    report = inventory.get_sales_report()

    for sku, stats in report.items():
        if stats['total_sold'] > 0:
            print(f"{stats['name']}:")
            print(f"  Sold: {stats['total_sold']} units")
            print(f"  Revenue: ${stats['revenue']:,.2f}")
            print(f"  Orders: {stats['order_count']}")
    print()

    # Test 8: Order history
    print("Test 8: Order History for LAP001")
    orders = inventory.get_order_history("LAP001")
    for order in orders:
        print(f"  {order.order_id}: {order.quantity} units - {order.status.value}")
    print()

    # Test 9: Add stock
    print("Test 9: Restocking")
    initial = inventory.get_stock_level("LAP001")
    inventory.add_stock("LAP001", 20)
    final = inventory.get_stock_level("LAP001")
    print(f"LAP001 stock: {initial} -> {final} (+20)\n")

    # Test 10: Out of stock
    print("Test 10: Out of Stock Items")
    inventory.add_product("OUT001", "Out of Stock Item", 0, 9.99)
    out_of_stock = inventory.get_out_of_stock_items()
    print(f"Out of stock: {[p.name for p in out_of_stock]}")
