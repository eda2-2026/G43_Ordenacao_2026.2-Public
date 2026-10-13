"""Merge Sort crescente e estável, sem alteração da entrada."""

from collections.abc import Callable, Sequence
from typing import TypeVar

from algorithms.metrics import SortMetrics

T = TypeVar("T")


def merge_sort(
    items: Sequence[T],
    *,
    key: Callable[[T], int],
    metrics: SortMetrics | None = None,
) -> list[T]:
    """Divide e intercala a lista, escolhendo a metade esquerda nos empates."""

    def divide(values: list[T]) -> list[T]:
        if len(values) <= 1:
            return values

        middle = len(values) // 2
        left = divide(values[:middle])
        right = divide(values[middle:])
        merged: list[T] = []
        left_index = right_index = 0

        while left_index < len(left) and right_index < len(right):
            if metrics is not None:
                metrics.comparisons += 1
            if key(left[left_index]) <= key(right[right_index]):
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1

        merged.extend(left[left_index:])
        merged.extend(right[right_index:])
        return merged

    return divide(list(items))
