"""Medição isolada, mediana, exportação e validações do benchmark."""

import csv
from io import StringIO
from statistics import median

import pytest

from benchmark.__main__ import main
from benchmark.runner import results_to_csv, run_benchmark
from services.catalog import sort_products
from services.generator import SCENARIOS, generate_products


def test_benchmark_covers_sizes_formats_and_algorithms():
    results = run_benchmark((10, 30), repetitions=2, seed=44)

    assert len(results) == 16
    assert {(row.quantity, row.scenario, row.algorithm) for row in results} == {
        (quantity, scenario, algorithm)
        for quantity in (10, 30)
        for scenario in SCENARIOS
        for algorithm in ("insertion", "merge")
    }
    for row in results:
        products = generate_products(row.quantity, scenario=row.scenario, seed=44)
        assert row.seed == 44 and row.repetitions == 2
        assert len(row.samples_ms) == 2
        assert all(sample >= 0 for sample in row.samples_ms)
        assert row.median_ms == median(row.samples_ms)
        assert row.comparisons == sort_products(products, row.algorithm).comparisons


def test_measurements_use_median_and_alternate_execution_order(monkeypatch):
    # Por formato: insertion recebe 9, 1, 3 ms; merge recebe 8, 2, 4 ms.
    durations_ms = [9, 8, 2, 1, 3, 4] * len(SCENARIOS)
    ticks = iter(value for duration in durations_ms for value in (0, duration * 1_000_000))
    monkeypatch.setattr("benchmark.runner.perf_counter_ns", lambda: next(ticks))

    results = run_benchmark((3,), repetitions=3)

    for row in results:
        expected = (9.0, 1.0, 3.0) if row.algorithm == "insertion" else (8.0, 2.0, 4.0)
        assert row.samples_ms == expected
        assert row.median_ms == (3.0 if row.algorithm == "insertion" else 4.0)
    assert next(ticks, None) is None


def test_generation_and_counting_are_outside_the_measured_interval(monkeypatch):
    state = {"measuring": False, "tick": 0}

    def clock():
        state["measuring"] = not state["measuring"]
        state["tick"] += 1
        return state["tick"] * 1_000_000

    def generate(*args, **kwargs):
        assert not state["measuring"]
        return generate_products(*args, **kwargs)

    def count(*args, **kwargs):
        assert not state["measuring"]
        return sort_products(*args, **kwargs)

    monkeypatch.setattr("benchmark.runner.perf_counter_ns", clock)
    monkeypatch.setattr("benchmark.runner.generate_products", generate)
    monkeypatch.setattr("benchmark.runner.sort_products", count)

    results = run_benchmark((10,), repetitions=1)

    assert len(results) == 8
    assert not state["measuring"]
    assert state["tick"] == 16


def test_csv_contains_the_same_metrics_and_individual_samples():
    results = run_benchmark((10,), repetitions=2, seed=44)
    rows = list(csv.DictReader(StringIO(results_to_csv(results))))

    assert len(rows) == len(results)
    for exported, result in zip(rows, results):
        assert int(exported["quantity"]) == result.quantity
        assert exported["scenario"] == result.scenario
        assert exported["algorithm"] == result.algorithm
        assert int(exported["seed"]) == 44
        assert int(exported["repetitions"]) == 2
        assert int(exported["comparisons"]) == result.comparisons
        assert float(exported["median_ms"]) == pytest.approx(result.median_ms, abs=0.000001)
        assert [float(value) for value in exported["samples_ms"].split(";")] == pytest.approx(
            result.samples_ms, abs=0.000001
        )


@pytest.mark.parametrize("sizes", [(), (0,), (-1,), (1001,), (True,), (1.5,), (10, 10)])
def test_invalid_sizes_are_rejected(sizes):
    with pytest.raises(ValueError, match="tamanhos"):
        run_benchmark(sizes)


@pytest.mark.parametrize("repetitions", [0, -1, 101, True, 1.5])
def test_invalid_repetition_count_is_rejected(repetitions):
    with pytest.raises(ValueError, match="repetições"):
        run_benchmark((10,), repetitions=repetitions)


@pytest.mark.parametrize("seed", [True, 1.5, "43", None])
def test_invalid_seed_is_rejected(seed):
    with pytest.raises(ValueError, match="semente"):
        run_benchmark((10,), seed=seed)


def test_cli_reports_all_formats(capsys):
    main(["--sizes", "10", "--repetitions", "1", "--seed", "44"])

    output = capsys.readouterr().out
    assert "Semente: 44" in output and "Repetições: 1" in output
    for scenario in SCENARIOS:
        assert scenario in output


def test_cli_rejects_invalid_configuration():
    with pytest.raises(SystemExit) as error:
        main(["--repetitions", "0"])
    assert error.value.code == 2
