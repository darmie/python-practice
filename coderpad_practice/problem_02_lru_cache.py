"""
Problem: Implement an LRU Cache

Implement a Least Recently Used (LRU) cache with O(1) operations.

Requirements:
1. get(key): Get value by key in O(1)
2. put(key, value): Insert/update key-value in O(1)
3. When capacity is reached, evict least recently used item
4. Both get and put count as "using" the item

Example:
    cache = LRUCache(capacity=2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)        # returns 1
    cache.put(3, 3)     # evicts key 2
    cache.get(2)        # returns None (not found)

Difficulty: Medium
Time: 30-40 minutes
Focus: Data structures, algorithm optimization
"""

from typing import Optional, Any


class Node:
    """Doubly linked list node for LRU cache."""

    def __init__(self, key: int, value: Any):
        self.key = key
        self.value = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


class LRUCache:
    """
    LRU Cache implementation using hashmap + doubly linked list.

    The hashmap provides O(1) lookup, while the doubly linked list
    maintains the order of usage (most recent at head, least recent at tail).
    """

    def __init__(self, capacity: int):
        """
        Initialize LRU cache with fixed capacity.

        Args:
            capacity: Maximum number of items in cache
        """
        self.capacity = capacity
        self.cache = {}  # key -> Node

        # Dummy head and tail for easier list manipulation
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> Optional[Any]:
        """
        Get value by key.

        Args:
            key: Cache key

        Returns:
            Value if found, None otherwise
        """
        if key not in self.cache:
            return None

        node = self.cache[key]

        # Move to front (most recently used)
        self._remove(node)
        self._add_to_front(node)

        return node.value

    def put(self, key: int, value: Any) -> None:
        """
        Insert or update key-value pair.

        Args:
            key: Cache key
            value: Value to store
        """
        # If key exists, update and move to front
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
            return

        # Create new node
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_front(node)

        # Check capacity
        if len(self.cache) > self.capacity:
            # Remove least recently used (tail)
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]

    def _remove(self, node: Node) -> None:
        """Remove node from linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node: Node) -> None:
        """Add node to front of linked list (most recently used)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def size(self) -> int:
        """Get current cache size."""
        return len(self.cache)

    def clear(self) -> None:
        """Clear all items from cache."""
        self.cache.clear()
        self.head.next = self.tail
        self.tail.prev = self.head

    def __repr__(self) -> str:
        """String representation of cache (for debugging)."""
        items = []
        current = self.head.next
        while current != self.tail:
            items.append(f"{current.key}:{current.value}")
            current = current.next
        return f"LRUCache({', '.join(items)})"


# Alternative: Using OrderedDict (Python 3.7+ maintains insertion order)
from collections import OrderedDict


class LRUCacheSimple:
    """
    Simpler LRU cache using OrderedDict.

    Note: While this is simpler, the custom implementation above
    better demonstrates understanding of data structures.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> Optional[Any]:
        if key not in self.cache:
            return None

        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            # Remove first item (least recently used)
            self.cache.popitem(last=False)


# Test cases
if __name__ == '__main__':
    print("Testing LRU Cache...")

    # Test 1: Basic operations
    print("\nTest 1: Basic operations")
    cache = LRUCache(capacity=2)

    cache.put(1, "one")
    cache.put(2, "two")
    print(f"After adding 1 and 2: {cache}")

    print(f"Get 1: {cache.get(1)}")
    print(f"Cache state: {cache}")

    cache.put(3, "three")  # Should evict key 2
    print(f"After adding 3: {cache}")

    print(f"Get 2 (should be None): {cache.get(2)}")

    # Test 2: Update existing key
    print("\nTest 2: Update existing key")
    cache = LRUCache(capacity=3)
    cache.put(1, "one")
    cache.put(2, "two")
    cache.put(3, "three")
    print(f"Initial: {cache}")

    cache.put(2, "TWO")  # Update
    print(f"After updating 2: {cache}")

    cache.put(4, "four")  # Should evict 1, not 2
    print(f"After adding 4: {cache}")
    print(f"Get 1 (should be None): {cache.get(1)}")

    # Test 3: Capacity = 1
    print("\nTest 3: Capacity = 1")
    cache = LRUCache(capacity=1)
    cache.put(1, "one")
    print(f"After adding 1: {cache}")

    cache.put(2, "two")
    print(f"After adding 2: {cache}")
    print(f"Get 1 (should be None): {cache.get(1)}")
    print(f"Get 2: {cache.get(2)}")

    # Test 4: Compare implementations
    print("\nTest 4: Comparing implementations")
    cache1 = LRUCache(capacity=3)
    cache2 = LRUCacheSimple(capacity=3)

    for i in range(5):
        cache1.put(i, f"value{i}")
        cache2.put(i, f"value{i}")

    print("Custom implementation:", cache1)
    print("OrderedDict implementation:", dict(cache2.cache))

    # Both should have keys 2, 3, 4
    assert cache1.get(2) == cache2.get(2) == "value2"
    assert cache1.get(0) == cache2.get(0) == None
    print("Both implementations match!")
