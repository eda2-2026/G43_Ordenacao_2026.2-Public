"""Geração reproduzível de produtos e formatos de entrada."""

import random

from algorithms.merge_sort import merge_sort
from models.product import Product

SCENARIOS = ("random", "ordered", "reversed", "nearly_ordered")
PRODUCT_NAMES = (
    "Teclado",
    "Mouse",
    "Monitor",
    "Fone de ouvido",
    "Webcam",
    "Carregador",
    "Cabo USB",
    "Suporte para notebook",
    "Caixa de som",
    "Pendrive",
)


def generate_products(
    quantity: int,
    *,
    scenario: str = "random",
    seed: int = 43,
) -> list[Product]:
    """Gera a mesma coleção por semente e altera somente sua ordem."""
    if type(quantity) is not int or not 0 <= quantity <= 1_000:
        raise ValueError("A quantidade deve ser um inteiro entre 0 e 1.000.")
    if scenario not in SCENARIOS:
        raise ValueError(f"Formato desconhecido: {scenario}. Opções: {', '.join(SCENARIOS)}.")
    if type(seed) is not int:
        raise ValueError("A semente deve ser um inteiro.")

    rng = random.Random(seed)
    products = [
        Product(
            identifier=index + 1,
            name=f"{PRODUCT_NAMES[index % len(PRODUCT_NAMES)]} {index + 1:04d}",
            price_cents=rng.randint(100, 50_000),
        )
        for index in range(quantity)
    ]

    if scenario == "random":
        return products

    ordered = merge_sort(products, key=lambda product: product.price_cents)
    if scenario == "reversed":
        return list(reversed(ordered))
    if scenario == "nearly_ordered":
        for index in range(0, len(ordered) - 1, 20):
            ordered[index], ordered[index + 1] = ordered[index + 1], ordered[index]
    return ordered
