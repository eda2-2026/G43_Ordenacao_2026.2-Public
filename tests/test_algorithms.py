"""Corretude e estabilidade das implementações manuais de ordenação."""

from itertools import product

import pytest

from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from algorithms.metrics import SortMetrics


@pytest.fixture(params=[insertion_sort, merge_sort], ids=["insertion", "merge"])
def sorter(request):
    return request.param


@pytest.mark.parametrize(
    "values",
    [[], [5], [2, 1], [3, 1, 2], [4, 4, 4], [-2, 0, -5, 3], list(range(20)), list(range(20, 0, -1))],
    ids=["empty", "single", "pair", "odd-length", "equal", "negative", "ordered", "reversed"],
)
def test_sort_matches_reference_without_changing_input(sorter, values):
    original = values.copy()

    actual = sorter(values, key=lambda value: value)

    assert actual == sorted(original)
    assert values == original
    assert actual is not values


def test_sort_accepts_immutable_sequence(sorter):
    assert sorter((3, 1, 2), key=lambda value: value) == [1, 2, 3]


def test_equal_keys_keep_original_objects_in_their_relative_order(sorter):
    records = [
        {"price": 200, "identifier": 9},
        {"price": 100, "identifier": 7},
        {"price": 200, "identifier": 1},
        {"price": 100, "identifier": 2},
    ]

    actual = sorter(records, key=lambda record: record["price"])

    assert [record["identifier"] for record in actual] == [7, 2, 9, 1]
    assert all(actual[index] is records[source] for index, source in enumerate([1, 3, 0, 2]))


def test_exhaustive_small_inputs_match_stable_reference(sorter):
    # Inclui todos os empates e disposições de três preços em listas de até seis itens.
    for size in range(7):
        for prices in product(range(3), repeat=size):
            records = [(price, size - index) for index, price in enumerate(prices)]
            expected = sorted(records, key=lambda record: record[0])

            actual = sorter(records, key=lambda record: record[0])

            assert actual == expected, f"Entrada: {records}"
            assert all(item is reference for item, reference in zip(actual, expected))


@pytest.mark.parametrize("values", [[], [10]], ids=["empty", "single"])
def test_small_inputs_require_no_key_comparisons(sorter, values):
    metrics = SortMetrics()

    sorter(values, key=lambda value: value, metrics=metrics)

    assert metrics.comparisons == 0


@pytest.mark.parametrize("size", [1, 2, 10, 100])
def test_insertion_comparison_counts_for_distinct_prices(size):
    ordered_metrics = SortMetrics()
    reversed_metrics = SortMetrics()

    insertion_sort(list(range(size)), key=lambda value: value, metrics=ordered_metrics)
    insertion_sort(list(range(size - 1, -1, -1)), key=lambda value: value, metrics=reversed_metrics)

    assert ordered_metrics.comparisons == size - 1
    assert reversed_metrics.comparisons == size * (size - 1) // 2


def test_merge_counts_key_comparisons_only():
    metrics = SortMetrics()

    actual = merge_sort([2, 1, 3], key=lambda value: value, metrics=metrics)

    assert actual == [1, 2, 3]
    assert metrics.comparisons == 3


def test_counting_does_not_change_sort_results(sorter):
    records = [(2, "A"), (1, "B"), (2, "C"), (1, "D")]
    metrics = SortMetrics()

    counted = sorter(records, key=lambda record: record[0], metrics=metrics)
    uncounted = sorter(records, key=lambda record: record[0])

    assert counted == uncounted == [(1, "B"), (1, "D"), (2, "A"), (2, "C")]
    assert metrics.comparisons > 0
