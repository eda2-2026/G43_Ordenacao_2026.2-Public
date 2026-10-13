"""Integração dos algoritmos com produtos e resultados independentes."""

import pytest

from models.product import Product
from services.catalog import compare_products, sort_products
from services.generator import generate_products


@pytest.fixture
def products():
    return [
        Product(9, "Teclado", 299),
        Product(2, "Mouse", 100),
        Product(7, "Webcam", 299),
        Product(1, "Cabo USB", 100),
        Product(4, "Brinde", 0),
    ]


@pytest.mark.parametrize("algorithm", ["insertion", "merge"])
def test_product_sort_uses_price_and_preserves_ties(algorithm, products):
    original = products.copy()

    result = sort_products(products, algorithm)

    assert result.algorithm == algorithm
    assert [item.identifier for item in result.products] == [4, 2, 1, 9, 7]
    assert products == original
    assert result.products is not products
    assert result.comparisons > 0


@pytest.mark.parametrize("algorithm", ["insertion", "merge"])
@pytest.mark.parametrize("size", [0, 1, 1000], ids=["empty", "single", "large"])
def test_product_sort_matches_reference_at_input_boundaries(algorithm, size):
    products = generate_products(size)
    original = products.copy()

    result = sort_products(products, algorithm)

    assert result.products == sorted(original, key=lambda item: item.price_cents)
    assert products == original
    assert [id(item) for item in result.products] == [
        id(item) for item in sorted(original, key=lambda item: item.price_cents)
    ]


@pytest.mark.parametrize("algorithm", ["insertion", "merge"])
def test_uncounted_sort_preserves_correctness_and_reports_no_metrics(algorithm, products):
    result = sort_products(tuple(products), algorithm, count_comparisons=False)

    assert result.products == sorted(products, key=lambda item: item.price_cents)
    assert result.comparisons is None


def test_comparison_results_do_not_share_lists_with_each_other_or_input(products):
    original = products.copy()

    insertion, merge = compare_products(products)

    assert insertion.algorithm == "insertion"
    assert merge.algorithm == "merge"
    assert insertion.products == merge.products == sorted(original, key=lambda item: item.price_cents)
    assert insertion.products is not merge.products
    insertion.products.clear()
    assert merge.products == sorted(original, key=lambda item: item.price_cents)
    assert products == original


def test_comparison_metrics_do_not_accumulate_between_calls(products):
    first = compare_products(products)
    second = compare_products(products)

    assert [result.comparisons for result in first] == [result.comparisons for result in second]


@pytest.mark.parametrize("algorithm", ["quick", "", "MERGE"])
def test_unknown_algorithm_is_rejected_even_for_empty_input(algorithm):
    with pytest.raises(ValueError, match="Algoritmo desconhecido"):
        sort_products([], algorithm)
