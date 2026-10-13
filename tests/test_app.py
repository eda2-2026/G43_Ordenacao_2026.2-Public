"""Integração da interface com os dados e os algoritmos de ordenação."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from services.catalog import compare_products
from services.generator import generate_products

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


@pytest.fixture
def app():
    return AppTest.from_file(APP_PATH, default_timeout=10).run()


def assert_displayed_results(app, quantity, scenario, seed):
    assert not app.exception
    products = generate_products(quantity, scenario=scenario, seed=seed)
    expected = sorted(products, key=lambda product: product.price_cents)
    positions = {product.identifier: index for index, product in enumerate(products, start=1)}

    assert len(app.dataframe) >= 3
    assert app.dataframe[0].value["ID"].tolist() == [product.identifier for product in products]
    for table in app.dataframe[1:3]:
        assert table.value["ID"].tolist() == [product.identifier for product in expected]
        assert table.value["Preço"].tolist() == [product.formatted_price for product in expected]
        assert table.value["Ordem original"].tolist() == [positions[product.identifier] for product in expected]

    results = compare_products(products)
    assert [metric.value for metric in app.metric] == [
        f"{result.comparisons:,}".replace(",", ".") for result in results
    ]


def test_initial_page_displays_a_complete_comparison(app):
    assert_displayed_results(app, 20, "random", 43)


@pytest.mark.parametrize(
    "quantity,scenario,seed",
    [(10, "random", 0), (1000, "ordered", 43), (30, "reversed", 44), (51, "nearly_ordered", 123)],
)
def test_form_updates_all_results_using_the_selected_configuration(app, quantity, scenario, seed):
    app.number_input(key="quantity").set_value(quantity)
    app.selectbox(key="scenario").set_value(scenario)
    app.number_input(key="seed").set_value(seed)
    app.button[0].click().run()

    assert_displayed_results(app, quantity, scenario, seed)
    assert any(f"{quantity} produtos" in caption.value and f"Semente {seed}" in caption.value for caption in app.caption)


def test_changing_controls_without_submission_keeps_the_displayed_data(app):
    app.number_input(key="quantity").set_value(100)
    app.selectbox(key="scenario").set_value("reversed")
    app.number_input(key="seed").set_value(44)
    app.run()

    assert_displayed_results(app, 20, "random", 43)
    assert any("20 produtos" in caption.value and "Semente 43" in caption.value for caption in app.caption)


def test_repeating_a_comparison_does_not_accumulate_metrics(app):
    first = [metric.value for metric in app.metric]

    app.button[0].click().run()

    assert not app.exception
    assert [metric.value for metric in app.metric] == first
    assert_displayed_results(app, 20, "random", 43)


def test_benchmark_runs_on_request_and_preserves_catalog_results(app):
    assert len(app.dataframe) == 3
    app.number_input(key="benchmark_repetitions").set_value(1)
    app.number_input(key="benchmark_seed").set_value(44)
    app.button[1].click().run(timeout=20)

    assert_displayed_results(app, 20, "random", 43)
    assert len(app.dataframe) == 4
    table = app.dataframe[3].value
    assert len(table) == 24
    assert set(table["Produtos"]) == {100, 500, 1000}
    assert set(table["Algoritmo"]) == {"Insertion Sort", "Merge Sort"}
    assert (table["Mediana (ms)"] >= 0).all()
    assert any("1 repetição" in caption.value and "Semente 44" in caption.value for caption in app.caption)

    original = table.copy()
    app.selectbox(key="benchmark_chart_scenario").set_value("ordered").run()
    assert not app.exception
    assert app.dataframe[3].value.equals(original)


def test_editing_benchmark_controls_does_not_replace_saved_measurements(app):
    app.number_input(key="benchmark_repetitions").set_value(1)
    app.button[1].click().run(timeout=20)
    original = app.dataframe[3].value.copy()

    app.number_input(key="benchmark_seed").set_value(123)
    app.run()

    assert not app.exception
    assert app.dataframe[3].value.equals(original)
    assert any("Benchmark exibido:" in caption.value and "Semente 43" in caption.value for caption in app.caption)
