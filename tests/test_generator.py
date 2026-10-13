"""Formatos de entrada, reprodução dos dados e validação do gerador."""

from collections import Counter
from math import ceil
import random

import pytest

from services.generator import SCENARIOS, generate_products


@pytest.mark.parametrize("scenario", SCENARIOS)
@pytest.mark.parametrize("quantity", [0, 1, 1000], ids=["empty", "single", "large"])
def test_generator_returns_valid_products_with_unique_identifiers(scenario, quantity):
    products = generate_products(quantity, scenario=scenario)

    assert len(products) == quantity
    assert len({item.identifier for item in products}) == quantity
    assert all(item.name.strip() and type(item.price_cents) is int and item.price_cents >= 0 for item in products)


@pytest.mark.parametrize("scenario", SCENARIOS)
@pytest.mark.parametrize("seed", [0, 43, -1])
def test_seed_reproduces_products_and_input_order(scenario, seed):
    assert generate_products(100, scenario=scenario, seed=seed) == generate_products(
        100, scenario=scenario, seed=seed
    )


def test_different_seeds_change_generated_prices():
    first = generate_products(100, seed=43)
    second = generate_products(100, seed=44)

    assert [item.price_cents for item in first] != [item.price_cents for item in second]


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_generation_does_not_modify_global_random_state(scenario):
    state = random.getstate()

    generate_products(100, scenario=scenario)

    assert random.getstate() == state


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_all_formats_contain_the_same_products(scenario):
    original = generate_products(100, seed=43)
    transformed = generate_products(100, scenario=scenario, seed=43)

    assert Counter(transformed) == Counter(original)


@pytest.mark.parametrize("scenario,descending", [("ordered", False), ("reversed", True)])
def test_ordered_formats_respect_price_order(scenario, descending):
    original = generate_products(100)
    actual = generate_products(100, scenario=scenario)

    expected_prices = sorted([item.price_cents for item in original], reverse=descending)
    assert [item.price_cents for item in actual] == expected_prices


def test_nearly_ordered_format_changes_only_a_small_number_of_neighbors():
    quantity = 200
    original = generate_products(quantity)
    ordered = sorted(original, key=lambda item: item.price_cents)
    nearly = generate_products(quantity, scenario="nearly_ordered")
    positions = {item.identifier: index for index, item in enumerate(ordered)}
    changed = sum(item != reference for item, reference in zip(nearly, ordered))

    assert 0 < changed <= 2 * ceil(quantity / 20)
    assert all(abs(positions[item.identifier] - index) <= 1 for index, item in enumerate(nearly))
    assert Counter(nearly) == Counter(ordered)


@pytest.mark.parametrize("quantity", [-1, 1001, 1.5, True, "10", None])
def test_invalid_quantity_is_rejected(quantity):
    with pytest.raises(ValueError, match="quantidade"):
        generate_products(quantity)


@pytest.mark.parametrize("scenario", ["invalid", "", None])
def test_unknown_scenario_is_rejected(scenario):
    with pytest.raises(ValueError, match="Formato desconhecido"):
        generate_products(10, scenario=scenario)


@pytest.mark.parametrize("seed", [1.5, True, "43", None])
def test_non_integer_seed_is_rejected(seed):
    with pytest.raises(ValueError, match="semente"):
        generate_products(10, seed=seed)
