"""
Lazy Evaluation and Generators
"""
from typing import Iterator, Iterable, Callable, Any
from itertools import islice, takewhile, dropwhile, accumulate


def fibonacci_generator() -> Iterator[int]:
    """
    Generate Fibonacci numbers lazily.

    Example:
        >>> fib = fibonacci_generator()
        >>> [next(fib) for _ in range(10)]
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def infinite_sequence(start: int = 0, step: int = 1) -> Iterator[int]:
    """
    Generate infinite sequence of numbers.

    Example:
        >>> seq = infinite_sequence(10, 5)
        >>> [next(seq) for _ in range(5)]
        [10, 15, 20, 25, 30]
    """
    current = start
    while True:
        yield current
        current += step


def lazy_map(func: Callable, iterable: Iterable) -> Iterator:
    """
    Lazy map implementation using generator.

    Example:
        >>> result = lazy_map(lambda x: x ** 2, range(5))
        >>> list(result)
        [0, 1, 4, 9, 16]
    """
    for item in iterable:
        yield func(item)


def lazy_filter(predicate: Callable, iterable: Iterable) -> Iterator:
    """
    Lazy filter implementation using generator.

    Example:
        >>> result = lazy_filter(lambda x: x % 2 == 0, range(10))
        >>> list(result)
        [0, 2, 4, 6, 8]
    """
    for item in iterable:
        if predicate(item):
            yield item


def take(n: int, iterable: Iterable) -> list:
    """
    Take first n items from iterable.

    Example:
        >>> take(5, fibonacci_generator())
        [0, 1, 1, 2, 3]
    """
    return list(islice(iterable, n))


def chunks(iterable: Iterable, size: int) -> Iterator:
    """
    Split iterable into chunks of given size.

    Example:
        >>> list(chunks(range(10), 3))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    iterator = iter(iterable)
    while True:
        chunk = list(islice(iterator, size))
        if not chunk:
            break
        yield chunk


def sliding_window(iterable: Iterable, size: int) -> Iterator:
    """
    Generate sliding windows over iterable.

    Example:
        >>> list(sliding_window([1, 2, 3, 4, 5], 3))
        [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    """
    iterator = iter(iterable)
    window = list(islice(iterator, size))

    if len(window) == size:
        yield list(window)

    for item in iterator:
        window = window[1:] + [item]
        yield list(window)


def prime_numbers() -> Iterator[int]:
    """
    Generate prime numbers lazily using Sieve of Eratosthenes.

    Example:
        >>> primes = prime_numbers()
        >>> [next(primes) for _ in range(10)]
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    def is_prime(n: int, primes: list) -> bool:
        for p in primes:
            if p * p > n:
                return True
            if n % p == 0:
                return False
        return True

    yield 2
    primes = [2]
    candidate = 3

    while True:
        if is_prime(candidate, primes):
            yield candidate
            primes.append(candidate)
        candidate += 2


def lazy_range_with_step(start: int, stop: int, step: int = 1) -> Iterator[int]:
    """
    Lazy range implementation.

    Example:
        >>> list(lazy_range_with_step(0, 10, 2))
        [0, 2, 4, 6, 8]
    """
    current = start
    while current < stop:
        yield current
        current += step


def batch_process(items: Iterable, batch_size: int, process_func: Callable) -> Iterator:
    """
    Process items in batches lazily.

    Example:
        >>> def process(batch):
        ...     return sum(batch)
        >>> list(batch_process(range(10), 3, process))
        [3, 12, 21, 9]
    """
    for chunk in chunks(items, batch_size):
        yield process_func(chunk)


def running_average(numbers: Iterable[float]) -> Iterator[float]:
    """
    Calculate running average lazily.

    Example:
        >>> list(running_average([1, 2, 3, 4, 5]))
        [1.0, 1.5, 2.0, 2.5, 3.0]
    """
    total = 0
    count = 0
    for num in numbers:
        total += num
        count += 1
        yield total / count
