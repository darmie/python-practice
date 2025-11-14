"""
Unit Tests for Algorithms and Data Structures

Run with: pytest testing/test_algorithms.py -v
"""
import pytest
from algorithms_and_data_structures.arrays_and_strings import (
    two_sum, reverse_string, is_palindrome,
    longest_substring_without_repeating, rotate_array, merge_sorted_arrays
)
from algorithms_and_data_structures.sorting_and_searching import (
    binary_search, quick_sort, merge_sort, find_kth_largest
)


class TestArraysAndStrings:
    """Test cases for array and string functions."""

    def test_two_sum_found(self):
        """Test two_sum when solution exists."""
        result = two_sum([2, 7, 11, 15], 9)
        assert result == [0, 1]

    def test_two_sum_not_found(self):
        """Test two_sum when no solution exists."""
        result = two_sum([1, 2, 3], 10)
        assert result is None

    def test_two_sum_empty_array(self):
        """Test two_sum with empty array."""
        result = two_sum([], 5)
        assert result is None

    @pytest.mark.parametrize("input_str,expected", [
        ("hello", "olleh"),
        ("", ""),
        ("a", "a"),
        ("racecar", "racecar"),
    ])
    def test_reverse_string(self, input_str, expected):
        """Test string reversal with multiple cases."""
        assert reverse_string(input_str) == expected

    @pytest.mark.parametrize("input_str,expected", [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        ("", True),
        ("a", True),
        ("ab", False),
    ])
    def test_is_palindrome(self, input_str, expected):
        """Test palindrome detection."""
        assert is_palindrome(input_str) == expected

    def test_longest_substring_without_repeating(self):
        """Test longest substring without repeating characters."""
        assert longest_substring_without_repeating("abcabcbb") == 3
        assert longest_substring_without_repeating("bbbbb") == 1
        assert longest_substring_without_repeating("pwwkew") == 3
        assert longest_substring_without_repeating("") == 0

    def test_rotate_array(self):
        """Test array rotation."""
        assert rotate_array([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
        assert rotate_array([1, 2], 3) == [2, 1]
        assert rotate_array([], 1) == []

    def test_merge_sorted_arrays(self):
        """Test merging sorted arrays."""
        assert merge_sorted_arrays([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
        assert merge_sorted_arrays([], [1, 2]) == [1, 2]
        assert merge_sorted_arrays([1, 2], []) == [1, 2]


class TestSortingAndSearching:
    """Test cases for sorting and searching algorithms."""

    def test_binary_search_found(self):
        """Test binary search when element is found."""
        assert binary_search([1, 2, 3, 4, 5, 6], 4) == 3
        assert binary_search([1, 2, 3, 4, 5, 6], 1) == 0
        assert binary_search([1, 2, 3, 4, 5, 6], 6) == 5

    def test_binary_search_not_found(self):
        """Test binary search when element is not found."""
        assert binary_search([1, 2, 3, 4, 5, 6], 7) == -1
        assert binary_search([], 1) == -1

    @pytest.mark.parametrize("sort_func", [quick_sort, merge_sort])
    def test_sorting_algorithms(self, sort_func):
        """Test sorting algorithms with same test cases."""
        assert sort_func([3, 6, 8, 10, 1, 2, 1]) == [1, 1, 2, 3, 6, 8, 10]
        assert sort_func([]) == []
        assert sort_func([1]) == [1]
        assert sort_func([2, 1]) == [1, 2]

    def test_find_kth_largest(self):
        """Test finding kth largest element."""
        assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
        assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_inputs(self):
        """Test functions with empty inputs."""
        assert two_sum([], 1) is None
        assert reverse_string("") == ""
        assert quick_sort([]) == []

    def test_single_element(self):
        """Test functions with single element."""
        assert quick_sort([1]) == [1]
        assert reverse_string("a") == "a"

    def test_large_inputs(self):
        """Test functions with large inputs."""
        large_array = list(range(1000, 0, -1))
        sorted_array = quick_sort(large_array)
        assert sorted_array == list(range(1, 1001))


@pytest.fixture
def sample_array():
    """Fixture providing sample array for tests."""
    return [5, 2, 8, 1, 9, 3]


def test_with_fixture(sample_array):
    """Test using fixture."""
    assert len(sample_array) == 6
    sorted_array = quick_sort(sample_array)
    assert sorted_array[0] == 1
    assert sorted_array[-1] == 9
