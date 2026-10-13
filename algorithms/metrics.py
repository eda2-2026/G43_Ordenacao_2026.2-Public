"""Métricas coletadas durante a ordenação."""

from dataclasses import dataclass


@dataclass
class SortMetrics:
    """Conta comparações entre chaves, sem incluir condições de laço."""

    comparisons: int = 0
