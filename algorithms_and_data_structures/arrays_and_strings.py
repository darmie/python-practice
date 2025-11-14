"""
Array and String manipulation problems
"""
from typing import List, Optional


def two_sum(nums: List[int], target: int) -> Optional[List[int]]:
    """
    Find two numbers in array that add up to target.

    Args:
        nums: List of integers
        target: Target sum

    Returns:
        List of two indices or None if not found

    Example:
        >>> two_sum([2, 7, 11, 15], 9)
        [0, 1]
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None


def reverse_string(s: str) -> str:
    """
    Reverse a string in place.

    Args:
        s: Input string

    Returns:
        Reversed string

    Example:
        >>> reverse_string("hello")
        'olleh'
    """
    return s[::-1]


def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome (ignoring case and non-alphanumeric).

    Args:
        s: Input string

    Returns:
        True if palindrome, False otherwise

    Example:
        >>> is_palindrome("A man, a plan, a canal: Panama")
        True
    """
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def longest_substring_without_repeating(s: str) -> int:
    """
    Find the length of longest substring without repeating characters.

    Args:
        s: Input string

    Returns:
        Length of longest substring

    Example:
        >>> longest_substring_without_repeating("abcabcbb")
        3
    """
    char_index = {}
    max_length = 0
    start = 0

    for i, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        char_index[char] = i
        max_length = max(max_length, i - start + 1)

    return max_length


def rotate_array(nums: List[int], k: int) -> List[int]:
    """
    Rotate array to the right by k steps.

    Args:
        nums: List of integers
        k: Number of steps to rotate

    Returns:
        Rotated array

    Example:
        >>> rotate_array([1, 2, 3, 4, 5, 6, 7], 3)
        [5, 6, 7, 1, 2, 3, 4]
    """
    if not nums:
        return nums

    k = k % len(nums)
    return nums[-k:] + nums[:-k] if k else nums


def merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    """
    Merge two sorted arrays into one sorted array.

    Args:
        arr1: First sorted array
        arr2: Second sorted array

    Returns:
        Merged sorted array

    Example:
        >>> merge_sorted_arrays([1, 3, 5], [2, 4, 6])
        [1, 2, 3, 4, 5, 6]
    """
    result = []
    i, j = 0, 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1

    result.extend(arr1[i:])
    result.extend(arr2[j:])

    return result
