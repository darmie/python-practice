"""
Linked List implementations and problems
"""
from typing import Optional


class ListNode:
    """Node in a singly-linked list."""

    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        return f"ListNode({self.val})"


class LinkedList:
    """Singly-linked list implementation."""

    def __init__(self):
        self.head: Optional[ListNode] = None

    def append(self, val: int) -> None:
        """Add a node to the end of the list."""
        if not self.head:
            self.head = ListNode(val)
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = ListNode(val)

    def to_list(self) -> list:
        """Convert linked list to Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.val)
            current = current.next
        return result

    @staticmethod
    def from_list(values: list) -> 'LinkedList':
        """Create linked list from Python list."""
        ll = LinkedList()
        for val in values:
            ll.append(val)
        return ll


def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverse a linked list.

    Args:
        head: Head of the linked list

    Returns:
        New head of reversed list

    Example:
        >>> ll = LinkedList.from_list([1, 2, 3, 4, 5])
        >>> reversed_head = reverse_linked_list(ll.head)
        >>> LinkedList.to_list_from_head(reversed_head)
        [5, 4, 3, 2, 1]
    """
    prev = None
    current = head

    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node

    return prev


def detect_cycle(head: Optional[ListNode]) -> bool:
    """
    Detect if linked list has a cycle using Floyd's algorithm.

    Args:
        head: Head of the linked list

    Returns:
        True if cycle exists, False otherwise
    """
    if not head or not head.next:
        return False

    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False


def merge_two_sorted_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Merge two sorted linked lists.

    Args:
        l1: Head of first sorted list
        l2: Head of second sorted list

    Returns:
        Head of merged sorted list
    """
    dummy = ListNode(0)
    current = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 if l1 else l2

    return dummy.next


def find_middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Find the middle node of a linked list.

    Args:
        head: Head of the linked list

    Returns:
        Middle node (if even length, return second middle)
    """
    if not head:
        return None

    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow
