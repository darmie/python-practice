"""
Higher-Order Functions and Function Composition
"""
from typing import Callable, List, Any, TypeVar
from functools import reduce

T = TypeVar('T')
U = TypeVar('U')


def compose(*functions: Callable) -> Callable:
    """
    Compose multiple functions into a single function.

    Args:
        *functions: Functions to compose (applied right to left)

    Returns:
        Composed function

    Example:
        >>> add_one = lambda x: x + 1
        >>> double = lambda x: x * 2
        >>> f = compose(double, add_one)
        >>> f(3)
        8
    """
    def inner(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result
    return inner


def pipe(*functions: Callable) -> Callable:
    """
    Pipe functions (compose left to right).

    Args:
        *functions: Functions to pipe (applied left to right)

    Returns:
        Piped function

    Example:
        >>> add_one = lambda x: x + 1
        >>> double = lambda x: x * 2
        >>> f = pipe(add_one, double)
        >>> f(3)
        8
    """
    def inner(arg):
        result = arg
        for func in functions:
            result = func(result)
        return result
    return inner


def curry(func: Callable) -> Callable:
    """
    Curry a function (simplified version for 2-arg functions).

    Example:
        >>> def add(x, y):
        ...     return x + y
        >>> curried_add = curry(add)
        >>> add_five = curried_add(5)
        >>> add_five(3)
        8
    """
    def curried(x):
        def inner(y):
            return func(x, y)
        return inner
    return curried


def map_filter_reduce_example(numbers: List[int]) -> int:
    """
    Example combining map, filter, and reduce.

    Example:
        >>> map_filter_reduce_example([1, 2, 3, 4, 5])
        48
    """
    # Map: square each number
    squared = list(map(lambda x: x ** 2, numbers))

    # Filter: keep only even numbers
    evens = list(filter(lambda x: x % 2 == 0, squared))

    # Reduce: sum all numbers
    total = reduce(lambda x, y: x + y, evens, 0)

    return total


def partial_application(func: Callable, *args: Any) -> Callable:
    """
    Create a partially applied function.

    Example:
        >>> def multiply(x, y, z):
        ...     return x * y * z
        >>> double = partial_application(multiply, 2)
        >>> double(3, 4)
        24
    """
    def inner(*more_args):
        return func(*args, *more_args)
    return inner


def memoize(func: Callable) -> Callable:
    """
    Memoization decorator for caching function results.

    Example:
        >>> @memoize
        ... def fibonacci(n):
        ...     if n <= 1:
        ...         return n
        ...     return fibonacci(n-1) + fibonacci(n-2)
        >>> fibonacci(10)
        55
    """
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


def flat_map(func: Callable[[T], List[U]], lst: List[T]) -> List[U]:
    """
    Apply function and flatten results.

    Example:
        >>> flat_map(lambda x: [x, x * 2], [1, 2, 3])
        [1, 2, 2, 4, 3, 6]
    """
    return [item for sublist in map(func, lst) for item in sublist]


def group_by(key_func: Callable[[T], Any], lst: List[T]) -> dict:
    """
    Group list items by key function.

    Example:
        >>> group_by(lambda x: x % 2, [1, 2, 3, 4, 5, 6])
        {1: [1, 3, 5], 0: [2, 4, 6]}
    """
    result = {}
    for item in lst:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result


def partition(predicate: Callable[[T], bool], lst: List[T]) -> tuple[List[T], List[T]]:
    """
    Partition list into two based on predicate.

    Example:
        >>> partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])
        ([2, 4, 6], [1, 3, 5])
    """
    true_items = []
    false_items = []

    for item in lst:
        if predicate(item):
            true_items.append(item)
        else:
            false_items.append(item)

    return true_items, false_items
