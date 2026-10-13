"""Integração dos algoritmos com o catálogo de produtos."""

from collections.abc import Sequence
from dataclasses import dataclass

from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from algorithms.metrics import SortMetrics
from models.product import Product

ALGORITHMS = {"insertion": insertion_sort, "merge": merge_sort}


@dataclass(frozen=True)
class SortResult:
    algorithm: str
    products: list[Product]
    comparisons: int | None


def sort_products(
    products: Sequence[Product],
    algorithm: str = "merge",
    *,
    count_comparisons: bool = True,
) -> SortResult:
    """Ordena por preço e, opcionalmente, registra comparações entre preços."""
    if algorithm not in ALGORITHMS:
        raise ValueError(f"Algoritmo desconhecido: {algorithm}. Opções: {', '.join(ALGORITHMS)}.")

    metrics = SortMetrics() if count_comparisons else None
    ordered = ALGORITHMS[algorithm](
        products,
        key=lambda product: product.price_cents,
        metrics=metrics,
    )
    return SortResult(
        algorithm=algorithm,
        products=ordered,
        comparisons=metrics.comparisons if metrics is not None else None,
    )


def compare_products(products: Sequence[Product]) -> tuple[SortResult, SortResult]:
    """Executa os dois algoritmos sobre a mesma entrada preservada."""
    original = list(products)
    return sort_products(original, "insertion"), sort_products(original, "merge")
