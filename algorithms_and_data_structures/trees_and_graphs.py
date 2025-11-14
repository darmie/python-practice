"""
Tree and Graph data structures and algorithms
"""
from typing import Optional, List
from collections import deque


class TreeNode:
    """Node in a binary tree."""

    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


class BinaryTree:
    """Binary tree implementation."""

    def __init__(self, root: Optional[TreeNode] = None):
        self.root = root

    def inorder_traversal(self, node: Optional[TreeNode] = None) -> List[int]:
        """Inorder traversal: Left -> Root -> Right"""
        if node is None:
            node = self.root

        if not node:
            return []

        result = []
        result.extend(self.inorder_traversal(node.left))
        result.append(node.val)
        result.extend(self.inorder_traversal(node.right))
        return result

    def preorder_traversal(self, node: Optional[TreeNode] = None) -> List[int]:
        """Preorder traversal: Root -> Left -> Right"""
        if node is None:
            node = self.root

        if not node:
            return []

        result = [node.val]
        result.extend(self.preorder_traversal(node.left))
        result.extend(self.preorder_traversal(node.right))
        return result

    def postorder_traversal(self, node: Optional[TreeNode] = None) -> List[int]:
        """Postorder traversal: Left -> Right -> Root"""
        if node is None:
            node = self.root

        if not node:
            return []

        result = []
        result.extend(self.postorder_traversal(node.left))
        result.extend(self.postorder_traversal(node.right))
        result.append(node.val)
        return result

    def level_order_traversal(self) -> List[List[int]]:
        """Level-order (BFS) traversal"""
        if not self.root:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            level_size = len(queue)
            level = []

            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level)

        return result


def max_depth(root: Optional[TreeNode]) -> int:
    """
    Find maximum depth of binary tree.

    Args:
        root: Root of the tree

    Returns:
        Maximum depth
    """
    if not root:
        return 0

    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)

    return max(left_depth, right_depth) + 1


def is_valid_bst(root: Optional[TreeNode], min_val: float = float('-inf'), max_val: float = float('inf')) -> bool:
    """
    Validate if tree is a valid Binary Search Tree.

    Args:
        root: Root of the tree
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        True if valid BST, False otherwise
    """
    if not root:
        return True

    if root.val <= min_val or root.val >= max_val:
        return False

    return (is_valid_bst(root.left, min_val, root.val) and
            is_valid_bst(root.right, root.val, max_val))


class Graph:
    """Graph implementation using adjacency list."""

    def __init__(self):
        self.graph = {}

    def add_edge(self, u: int, v: int, directed: bool = False):
        """Add an edge to the graph."""
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

        if not directed:
            if v not in self.graph:
                self.graph[v] = []
            self.graph[v].append(u)

    def bfs(self, start: int) -> List[int]:
        """Breadth-First Search traversal."""
        if start not in self.graph:
            return []

        visited = set()
        queue = deque([start])
        result = []

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                result.append(node)

                for neighbor in self.graph.get(node, []):
                    if neighbor not in visited:
                        queue.append(neighbor)

        return result

    def dfs(self, start: int) -> List[int]:
        """Depth-First Search traversal."""
        if start not in self.graph:
            return []

        visited = set()
        result = []

        def dfs_helper(node: int):
            visited.add(node)
            result.append(node)

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    dfs_helper(neighbor)

        dfs_helper(start)
        return result

    def has_cycle(self) -> bool:
        """Detect if graph has a cycle (for directed graph)."""
        visited = set()
        rec_stack = set()

        def has_cycle_helper(node: int) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle_helper(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in self.graph:
            if node not in visited:
                if has_cycle_helper(node):
                    return True

        return False
