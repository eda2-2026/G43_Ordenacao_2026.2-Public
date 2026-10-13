"""Execução do benchmark pelo comando python -m benchmark."""

import argparse
from collections.abc import Sequence
from pathlib import Path
import platform

from benchmark.runner import DEFAULT_SIZES, results_to_csv, run_benchmark


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Compara Insertion Sort e Merge Sort nos quatro formatos de entrada.")
    parser.add_argument("--sizes", type=int, nargs="+", default=DEFAULT_SIZES, help="Quantidades de produtos (1 a 1.000).")
    parser.add_argument("--repetitions", type=int, default=5, help="Repetições por cenário (1 a 100).")
    parser.add_argument("--seed", type=int, default=43, help="Semente dos produtos fictícios.")
    parser.add_argument("--csv", type=Path, help="Caminho do arquivo CSV de resultados.")
    args = parser.parse_args(argv)

    try:
        results = run_benchmark(args.sizes, repetitions=args.repetitions, seed=args.seed)
    except ValueError as error:
        parser.error(str(error))

    print(f"Python {platform.python_version()} ({platform.python_implementation()}) | {platform.system()} {platform.machine()}")
    print(f"Semente: {args.seed} | Repetições: {args.repetitions} | Tempos em milissegundos (mediana)")
    print(f"{'Produtos':>8} | {'Entrada':<15} | {'Algoritmo':<9} | {'Mediana (ms)':>12} | {'Comparações':>11}")
    for result in results:
        print(
            f"{result.quantity:8d} | {result.scenario:<15} | {result.algorithm:<9} | "
            f"{result.median_ms:12.6f} | {result.comparisons:11d}"
        )

    if args.csv is not None:
        try:
            args.csv.write_text(results_to_csv(results), encoding="utf-8", newline="")
        except OSError as error:
            parser.exit(1, f"Não foi possível salvar o CSV: {error}\n")
        print(f"CSV salvo em: {args.csv}")


if __name__ == "__main__":
    main()
