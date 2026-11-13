"""Standard, production-grade, bug-free binary search implementation."""
from typing import Sequence, TypeVar

T = TypeVar("T")


def binary_search(array: Sequence[T], target: T) -> int | None:
    """Perform binary search on a sorted sequence.

    Args:
        array: A sorted sequence of comparable elements.
        target: The element to locate.

    Returns:
        The zero-based index of target if present, else None.
    """
    left: int = 0
    right: int = len(array) - 1

    while left <= right:
        # Standard overflow-safe midpoint calculation
        mid: int = left + (right - left) // 2
        mid_val = array[mid]

        if mid_val == target:
            return mid
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return None
