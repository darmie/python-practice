"""
Common Helper Functions
"""
import time
from functools import wraps
from typing import Callable, Any
import json


def timer(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.

    Example:
        @timer
        def slow_function():
            time.sleep(1)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry a function on failure.

    Example:
        @retry(max_attempts=3, delay=1.0)
        def unreliable_function():
            # might fail
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator


def validate_type(expected_type: type):
    """
    Decorator to validate function return type.

    Example:
        @validate_type(int)
        def get_number():
            return 42
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not isinstance(result, expected_type):
                raise TypeError(
                    f"Expected {expected_type.__name__}, "
                    f"got {type(result).__name__}"
                )
            return result
        return wrapper
    return decorator


def singleton(cls):
    """
    Decorator to make a class a singleton.

    Example:
        @singleton
        class DatabaseConnection:
            pass
    """
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def read_json_file(file_path: str) -> dict:
    """Read and parse JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def write_json_file(file_path: str, data: dict) -> None:
    """Write data to JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def flatten_list(nested_list: list) -> list:
    """
    Flatten a nested list.

    Example:
        >>> flatten_list([[1, 2], [3, 4], [5]])
        [1, 2, 3, 4, 5]
    """
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def chunk_list(lst: list, chunk_size: int) -> list:
    """
    Split list into chunks.

    Example:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


class classproperty:
    """
    Decorator for class-level properties.

    Example:
        class MyClass:
            _value = 42

            @classproperty
            def value(cls):
                return cls._value
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, owner):
        return self.func(owner)
