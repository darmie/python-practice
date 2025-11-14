"""
Sorting and Searching algorithms
"""
from typing import List, Optional


def binary_search(arr: List[int], target: int) -> int:
    """
    Binary search in sorted array.

    Args:
        arr: Sorted array
        target: Value to find

    Returns:
        Index of target or -1 if not found

    Example:
        >>> binary_search([1, 2, 3, 4, 5, 6], 4)
        3
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def quick_sort(arr: List[int]) -> List[int]:
    """
    Quick sort implementation.

    Args:
        arr: Array to sort

    Returns:
        Sorted array

    Example:
        >>> quick_sort([3, 6, 8, 10, 1, 2, 1])
        [1, 1, 2, 3, 6, 8, 10]
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def merge_sort(arr: List[int]) -> List[int]:
    """
    Merge sort implementation.

    Args:
        arr: Array to sort

    Returns:
        Sorted array

    Example:
        >>> merge_sort([38, 27, 43, 3, 9, 82, 10])
        [3, 9, 10, 27, 38, 43, 82]
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left: List[int], right: List[int]) -> List[int]:
    """Helper function for merge sort."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def find_kth_largest(nums: List[int], k: int) -> Optional[int]:
    """
    Find the kth largest element in an array.

    Args:
        nums: Array of integers
        k: Position (1-indexed)

    Returns:
        The kth largest element

    Example:
        >>> find_kth_largest([3, 2, 1, 5, 6, 4], 2)
        5
    """
    if not nums or k < 1 or k > len(nums):
        return None

    sorted_nums = sorted(nums, reverse=True)
    return sorted_nums[k - 1]


def search_in_rotated_array(nums: List[int], target: int) -> int:
    """
    Search in a rotated sorted array.

    Args:
        nums: Rotated sorted array
        target: Value to find

    Returns:
        Index of target or -1 if not found

    Example:
        >>> search_in_rotated_array([4, 5, 6, 7, 0, 1, 2], 0)
        4
    """
    if not nums:
        return -1

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Find k most frequent elements.

    Args:
        nums: Array of integers
        k: Number of top frequent elements

    Returns:
        List of k most frequent elements

    Example:
        >>> top_k_frequent([1, 1, 1, 2, 2, 3], 2)
        [1, 2]
    """
    from collections import Counter

    count = Counter(nums)
    return [num for num, _ in count.most_common(k)]
