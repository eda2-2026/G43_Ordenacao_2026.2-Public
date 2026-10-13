"""Validação dos produtos e representação monetária sem arredondamento."""

from dataclasses import FrozenInstanceError

import pytest

from models.product import Product


@pytest.mark.parametrize(
    "price_cents,expected",
    [(0, "R$ 0,00"), (1, "R$ 0,01"), (99, "R$ 0,99"), (100, "R$ 1,00"), (100000001, "R$ 1.000.000,01")],
)
def test_price_formatting_preserves_cents(price_cents, expected):
    assert Product(1, "Produto", price_cents).formatted_price == expected


@pytest.mark.parametrize("identifier", [0, -1, 1.5, True, "1"])
def test_invalid_identifier_is_rejected(identifier):
    with pytest.raises(ValueError, match="identificador"):
        Product(identifier, "Produto", 100)


@pytest.mark.parametrize("name", ["", "   ", None, 42])
def test_invalid_name_is_rejected(name):
    with pytest.raises(ValueError, match="nome"):
        Product(1, name, 100)


@pytest.mark.parametrize("price_cents", [-1, 1.5, True, "100"])
def test_invalid_price_is_rejected(price_cents):
    with pytest.raises(ValueError, match="preço"):
        Product(1, "Produto", price_cents)


def test_product_price_cannot_be_changed_after_creation():
    product = Product(1, "Produto", 100)

    with pytest.raises(FrozenInstanceError):
        product.price_cents = 200

    assert product.price_cents == 100
