"""
Immutability and Pure Functions
"""
from typing import List, Any, TypeVar
from dataclasses import dataclass, replace
from copy import deepcopy

T = TypeVar('T')


@dataclass(frozen=True)
class ImmutablePoint:
    """
    Immutable point using frozen dataclass.

    Example:
        >>> p = ImmutablePoint(1, 2)
        >>> p.x
        1
        >>> # p.x = 3  # This would raise an error
    """
    x: float
    y: float

    def move(self, dx: float, dy: float) -> 'ImmutablePoint':
        """Create new point with offset."""
        return ImmutablePoint(self.x + dx, self.y + dy)

    def distance_from_origin(self) -> float:
        """Calculate distance from origin (pure function)."""
        return (self.x ** 2 + self.y ** 2) ** 0.5


def pure_sum(numbers: List[int]) -> int:
    """
    Pure function: always returns same output for same input.
    No side effects.

    Example:
        >>> pure_sum([1, 2, 3, 4, 5])
        15
    """
    return sum(numbers)


def impure_example():
    """
    Example of impure function (for demonstration).
    Modifies external state.
    """
    global counter
    counter += 1
    return counter


counter = 0


def append_immutable(lst: List[T], item: T) -> List[T]:
    """
    Append to list without modifying original.

    Example:
        >>> original = [1, 2, 3]
        >>> new_list = append_immutable(original, 4)
        >>> new_list
        [1, 2, 3, 4]
        >>> original
        [1, 2, 3]
    """
    return lst + [item]


def remove_immutable(lst: List[T], item: T) -> List[T]:
    """
    Remove from list without modifying original.

    Example:
        >>> original = [1, 2, 3, 2, 4]
        >>> new_list = remove_immutable(original, 2)
        >>> new_list
        [1, 3, 4]
    """
    return [x for x in lst if x != item]


def update_dict_immutable(d: dict, key: str, value: Any) -> dict:
    """
    Update dictionary without modifying original.

    Example:
        >>> original = {'a': 1, 'b': 2}
        >>> updated = update_dict_immutable(original, 'c', 3)
        >>> updated
        {'a': 1, 'b': 2, 'c': 3}
        >>> original
        {'a': 1, 'b': 2}
    """
    new_dict = d.copy()
    new_dict[key] = value
    return new_dict


@dataclass(frozen=True)
class ImmutablePerson:
    """Immutable person object."""
    name: str
    age: int
    email: str

    def update_email(self, new_email: str) -> 'ImmutablePerson':
        """Create new person with updated email."""
        return replace(self, email=new_email)

    def celebrate_birthday(self) -> 'ImmutablePerson':
        """Create new person with incremented age."""
        return replace(self, age=self.age + 1)


def deep_copy_example(nested_list: List[List[int]]) -> List[List[int]]:
    """
    Create deep copy of nested structure.

    Example:
        >>> original = [[1, 2], [3, 4]]
        >>> copied = deep_copy_example(original)
        >>> copied[0][0] = 99
        >>> original[0][0]
        1
    """
    return deepcopy(nested_list)


def chain_operations(data: List[int]) -> List[int]:
    """
    Chain multiple immutable operations.

    Example:
        >>> chain_operations([1, 2, 3, 4, 5])
        [4, 16, 36]
    """
    # Filter even numbers
    result = [x for x in data if x % 2 == 0]
    # Square them
    result = [x ** 2 for x in result]
    # Remove items less than 10
    result = [x for x in result if x >= 10]
    return result
