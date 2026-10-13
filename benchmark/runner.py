"""Medições repetidas de ordenação, sem geração ou contagem no intervalo medido."""

from collections.abc import Sequence
import csv
from dataclasses import dataclass
from io import StringIO
from statistics import median
from time import perf_counter_ns

from services.catalog import ALGORITHMS, sort_products
from services.generator import SCENARIOS, generate_products

DEFAULT_SIZES = (100, 500, 1000)


@dataclass(frozen=True)
class BenchmarkResult:
    quantity: int
    scenario: str
    algorithm: str
    repetitions: int
    seed: int
    median_ms: float
    comparisons: int
    samples_ms: tuple[float, ...]


def run_benchmark(
    sizes: Sequence[int] = DEFAULT_SIZES,
    *,
    repetitions: int = 5,
    seed: int = 43,
) -> list[BenchmarkResult]:
    """Compara os dois algoritmos em cópias da mesma entrada, nos quatro formatos."""
    if not sizes or any(type(size) is not int or not 1 <= size <= 1000 for size in sizes):
        raise ValueError("Os tamanhos devem ser inteiros entre 1 e 1.000.")
    if len(set(sizes)) != len(sizes):
        raise ValueError("Os tamanhos não podem ser repetidos.")
    if type(repetitions) is not int or not 1 <= repetitions <= 100:
        raise ValueError("As repetições devem ser um inteiro entre 1 e 100.")
    if type(seed) is not int:
        raise ValueError("A semente deve ser um inteiro.")

    results = []
    algorithms = tuple(ALGORITHMS)
    price_key = lambda product: product.price_cents

    for quantity in sizes:
        for scenario in SCENARIOS:
            products = generate_products(quantity, scenario=scenario, seed=seed)
            samples = {algorithm: [] for algorithm in algorithms}

            # Uma execução de aquecimento por algoritmo, fora do intervalo medido.
            for algorithm in algorithms:
                ALGORITHMS[algorithm](products, key=price_key)

            for repetition in range(repetitions):
                # Alterna quem executa primeiro para reduzir o efeito da ordem de execução.
                order = algorithms if repetition % 2 == 0 else algorithms[::-1]
                for algorithm in order:
                    sorter = ALGORITHMS[algorithm]
                    start = perf_counter_ns()
                    ordered = sorter(products, key=price_key)
                    elapsed_ns = perf_counter_ns() - start
                    samples[algorithm].append(elapsed_ns / 1_000_000)
                    # A liberação do resultado também ocorre fora do intervalo medido.
                    del ordered

            for algorithm in algorithms:
                counted = sort_products(products, algorithm)
                results.append(
                    BenchmarkResult(
                        quantity=quantity,
                        scenario=scenario,
                        algorithm=algorithm,
                        repetitions=repetitions,
                        seed=seed,
                        median_ms=median(samples[algorithm]),
                        comparisons=counted.comparisons,
                        samples_ms=tuple(samples[algorithm]),
                    )
                )

    return results


def results_to_csv(results: Sequence[BenchmarkResult]) -> str:
    """Exporta medianas e amostras individuais em milissegundos."""
    output = StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(
        ["quantity", "scenario", "algorithm", "repetitions", "seed", "median_ms", "comparisons", "samples_ms"]
    )
    for result in results:
        writer.writerow(
            [
                result.quantity,
                result.scenario,
                result.algorithm,
                result.repetitions,
                result.seed,
                f"{result.median_ms:.6f}",
                result.comparisons,
                ";".join(f"{sample:.6f}" for sample in result.samples_ms),
            ]
        )
    return output.getvalue()
