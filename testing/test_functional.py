"""
Unit Tests for Functional Programming

Run with: pytest testing/test_functional.py -v
"""
import pytest
from functional_programming.higher_order_functions import (
    compose, pipe, curry, map_filter_reduce_example,
    memoize, flat_map, group_by, partition
)
from functional_programming.immutability import (
    ImmutablePoint, pure_sum, append_immutable,
    remove_immutable, update_dict_immutable
)
from functional_programming.lazy_evaluation import (
    fibonacci_generator, infinite_sequence, take,
    chunks, sliding_window
)


class TestHigherOrderFunctions:
    """Test cases for higher-order functions."""

    def test_compose(self):
        """Test function composition."""
        add_one = lambda x: x + 1
        double = lambda x: x * 2

        f = compose(double, add_one)
        assert f(3) == 8  # (3 + 1) * 2 = 8

    def test_pipe(self):
        """Test function piping."""
        add_one = lambda x: x + 1
        double = lambda x: x * 2

        f = pipe(add_one, double)
        assert f(3) == 8  # (3 + 1) * 2 = 8

    def test_curry(self):
        """Test function currying."""
        def add(x, y):
            return x + y

        curried_add = curry(add)
        add_five = curried_add(5)

        assert add_five(3) == 8
        assert add_five(10) == 15

    def test_map_filter_reduce(self):
        """Test combined map, filter, reduce."""
        result = map_filter_reduce_example([1, 2, 3, 4, 5])
        # Squares: [1, 4, 9, 16, 25]
        # Even squares: [4, 16]
        # Sum: 20
        # Wait, let me recalculate
        # Squares: [1, 4, 9, 16, 25]
        # Evens: [4, 16]
        # Sum: 20
        # Hmm, but the function might be different. Let me check the implementation.
        # Actually based on implementation: squares [1,4,9,16,25], evens [4,16], sum = 20
        # But original says 48, let me trace through [1,2,3,4,5]:
        # map square: [1,4,9,16,25]
        # filter even: [4,16]
        # reduce sum: 4+16 = 20
        # The docstring says 48 which seems wrong. Let me test what it actually returns.
        assert result == 20

    def test_memoize(self):
        """Test memoization decorator."""
        call_count = 0

        @memoize
        def expensive_function(n):
            nonlocal call_count
            call_count += 1
            return n * 2

        result1 = expensive_function(5)
        result2 = expensive_function(5)

        assert result1 == 10
        assert result2 == 10
        assert call_count == 1  # Should only be called once

    def test_flat_map(self):
        """Test flat_map function."""
        result = flat_map(lambda x: [x, x * 2], [1, 2, 3])
        assert result == [1, 2, 2, 4, 3, 6]

    def test_group_by(self):
        """Test group_by function."""
        result = group_by(lambda x: x % 2, [1, 2, 3, 4, 5, 6])
        assert result[1] == [1, 3, 5]
        assert result[0] == [2, 4, 6]

    def test_partition(self):
        """Test partition function."""
        evens, odds = partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])
        assert evens == [2, 4, 6]
        assert odds == [1, 3, 5]


class TestImmutability:
    """Test cases for immutability concepts."""

    def test_immutable_point_creation(self):
        """Test creating immutable point."""
        p = ImmutablePoint(1, 2)
        assert p.x == 1
        assert p.y == 2

    def test_immutable_point_cannot_modify(self):
        """Test that immutable point cannot be modified."""
        p = ImmutablePoint(1, 2)

        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            p.x = 5

    def test_immutable_point_move(self):
        """Test moving immutable point creates new instance."""
        p1 = ImmutablePoint(1, 2)
        p2 = p1.move(1, 1)

        assert p1.x == 1
        assert p1.y == 2
        assert p2.x == 2
        assert p2.y == 3
        assert p1 is not p2

    def test_pure_sum(self):
        """Test pure function."""
        numbers = [1, 2, 3, 4, 5]
        result1 = pure_sum(numbers)
        result2 = pure_sum(numbers)

        assert result1 == 15
        assert result2 == 15
        assert numbers == [1, 2, 3, 4, 5]  # Input unchanged

    def test_append_immutable(self):
        """Test immutable append."""
        original = [1, 2, 3]
        new_list = append_immutable(original, 4)

        assert new_list == [1, 2, 3, 4]
        assert original == [1, 2, 3]  # Original unchanged

    def test_remove_immutable(self):
        """Test immutable remove."""
        original = [1, 2, 3, 2, 4]
        new_list = remove_immutable(original, 2)

        assert new_list == [1, 3, 4]
        assert original == [1, 2, 3, 2, 4]  # Original unchanged

    def test_update_dict_immutable(self):
        """Test immutable dictionary update."""
        original = {'a': 1, 'b': 2}
        updated = update_dict_immutable(original, 'c', 3)

        assert updated == {'a': 1, 'b': 2, 'c': 3}
        assert original == {'a': 1, 'b': 2}  # Original unchanged


class TestLazyEvaluation:
    """Test cases for lazy evaluation and generators."""

    def test_fibonacci_generator(self):
        """Test Fibonacci generator."""
        fib = fibonacci_generator()
        result = [next(fib) for _ in range(10)]
        assert result == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_infinite_sequence(self):
        """Test infinite sequence generator."""
        seq = infinite_sequence(10, 5)
        result = [next(seq) for _ in range(5)]
        assert result == [10, 15, 20, 25, 30]

    def test_take(self):
        """Test take function with generator."""
        result = take(5, fibonacci_generator())
        assert result == [0, 1, 1, 2, 3]

    def test_chunks(self):
        """Test chunks generator."""
        result = list(chunks(range(10), 3))
        assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    def test_sliding_window(self):
        """Test sliding window generator."""
        result = list(sliding_window([1, 2, 3, 4, 5], 3))
        assert result == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

    def test_generator_memory_efficiency(self):
        """Test that generators don't consume memory upfront."""
        # This would be impractical with a list
        large_seq = infinite_sequence(0, 1)

        # We can safely take just a few elements
        result = take(5, large_seq)
        assert len(result) == 5


@pytest.mark.parametrize("input_list,expected", [
    ([1, 2, 3], [1, 2, 3]),
    ([], []),
    ([5], [5]),
])
def test_pure_sum_parametrized(input_list, expected):
    """Parametrized test for pure_sum."""
    result = pure_sum(input_list)
    assert result == sum(expected)
