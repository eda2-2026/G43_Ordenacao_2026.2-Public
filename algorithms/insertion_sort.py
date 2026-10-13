"""Insertion Sort crescente e estável, sem alteração da entrada."""

from collections.abc import Callable, Sequence
from typing import TypeVar

from algorithms.metrics import SortMetrics

T = TypeVar("T")


def insertion_sort(
    items: Sequence[T],
    *,
    key: Callable[[T], int],
    metrics: SortMetrics | None = None,
) -> list[T]:
    """Insere cada item no prefixo ordenado; empates não são deslocados."""
    ordered = list(items)

    for position in range(1, len(ordered)):
        current = ordered[position]
        current_key = key(current)
        previous = position - 1

        while previous >= 0:
            if metrics is not None:
                metrics.comparisons += 1
            if key(ordered[previous]) <= current_key:
                break
            ordered[previous + 1] = ordered[previous]
            previous -= 1

        ordered[previous + 1] = current

    return ordered
