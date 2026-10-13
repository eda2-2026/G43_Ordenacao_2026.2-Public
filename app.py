"""Interface comparativa de ordenação de produtos do grupo 43."""

import streamlit as st

from benchmark.runner import DEFAULT_SIZES, results_to_csv, run_benchmark
from models.product import Product
from services.catalog import SortResult, compare_products
from services.generator import generate_products

SCENARIO_LABELS = {
    "random": "Aleatória",
    "ordered": "Ordenada",
    "reversed": "Invertida",
    "nearly_ordered": "Quase ordenada",
}
ALGORITHM_LABELS = {"insertion": "Insertion Sort", "merge": "Merge Sort"}


def render_benchmark() -> None:
    st.divider()
    st.subheader("Benchmark de desempenho")
    st.write(
        "Compare o tempo de ordenação de 100, 500 e 1.000 produtos nos quatro formatos "
        "de entrada. O resultado é a mediana das repetições para cada algoritmo."
    )
    with st.form("benchmark_settings"):
        repetitions_column, seed_column = st.columns(2)
        with repetitions_column:
            repetitions = st.number_input(
                "Repetições por cenário",
                min_value=1,
                max_value=15,
                value=5,
                step=1,
                key="benchmark_repetitions",
            )
        with seed_column:
            seed = st.number_input(
                "Semente do benchmark",
                min_value=0,
                max_value=2_147_483_647,
                value=43,
                step=1,
                key="benchmark_seed",
            )
        submitted = st.form_submit_button("Executar benchmark")

    if submitted:
        with st.spinner("Medindo os algoritmos..."):
            results = run_benchmark(repetitions=repetitions, seed=seed)
        st.session_state["benchmark_report"] = {
            "results": results,
            "repetitions": repetitions,
            "seed": seed,
        }

    if "benchmark_report" not in st.session_state:
        return

    report = st.session_state["benchmark_report"]
    results = report["results"]
    repetition_label = "repetição" if report["repetitions"] == 1 else "repetições"
    st.caption(
        f"Benchmark exibido: {report['repetitions']} {repetition_label} por cenário · "
        f"Semente {report['seed']} · Uma execução de aquecimento por algoritmo"
    )
    st.dataframe(
        [
            {
                "Produtos": result.quantity,
                "Entrada": SCENARIO_LABELS[result.scenario],
                "Algoritmo": ALGORITHM_LABELS[result.algorithm],
                "Mediana (ms)": result.median_ms,
                "Comparações": result.comparisons,
            }
            for result in results
        ],
        hide_index=True,
        width="stretch",
        column_config={"Mediana (ms)": st.column_config.NumberColumn(format="%.4f")},
        key="benchmark_table",
    )

    scenario = st.selectbox(
        "Formato no gráfico de tempos",
        options=list(SCENARIO_LABELS),
        format_func=SCENARIO_LABELS.get,
        key="benchmark_chart_scenario",
    )
    chart = {"Produtos": list(DEFAULT_SIZES)}
    for algorithm, label in ALGORITHM_LABELS.items():
        chart[label] = [
            result.median_ms
            for result in results
            if result.scenario == scenario and result.algorithm == algorithm
        ]
    st.line_chart(chart, x="Produtos", y=list(ALGORITHM_LABELS.values()), y_label="Mediana (ms)")
    st.caption(
        "A geração de dados, a contagem de comparações e a interface ficam fora do tempo "
        "medido. Os tempos incluem a cópia da entrada feita pelos algoritmos e variam "
        "conforme o computador e os processos em execução."
    )
    st.download_button(
        "Baixar resultados em CSV",
        data=results_to_csv(results),
        file_name="benchmark_ordenacao.csv",
        mime="text/csv",
        on_click="ignore",
    )


def product_rows(
    products: list[Product],
    original_positions: dict[int, int] | None = None,
) -> list[dict]:
    rows = []
    for position, product in enumerate(products, start=1):
        row = {"Posição": position}
        if original_positions is not None:
            row["Ordem original"] = original_positions[product.identifier]
        row.update(
            {"ID": product.identifier, "Produto": product.name, "Preço": product.formatted_price}
        )
        rows.append(row)
    return rows


def render_result(
    title: str,
    result: SortResult,
    original_positions: dict[int, int],
) -> None:
    st.subheader(title)
    st.metric("Comparações de preço", f"{result.comparisons:,}".replace(",", "."))
    st.dataframe(
        product_rows(result.products, original_positions),
        hide_index=True,
        height=380,
        width="stretch",
        key=f"{result.algorithm}_table",
    )


def main() -> None:
    st.set_page_config(
        page_title="Catálogo de Produtos | Grupo 43",
        page_icon="🛒",
        layout="wide",
    )

    st.title("🛒 Catálogo de Produtos")
    st.caption("Estruturas de Dados 2 · Trabalho 2: Ordenação · Grupo 43")

    st.write(
        "Este projeto compara Insertion Sort e Merge Sort na ordenação "
        "de produtos por preço, usando a mesma lista de entrada para os dois algoritmos."
    )

    with st.form("catalog_settings"):
        quantity_column, scenario_column, seed_column = st.columns(3)
        with quantity_column:
            quantity = st.number_input(
                "Quantidade de produtos",
                min_value=10,
                max_value=1000,
                value=20,
                step=10,
                key="quantity",
            )
        with scenario_column:
            scenario = st.selectbox(
                "Formato da entrada",
                options=list(SCENARIO_LABELS),
                format_func=SCENARIO_LABELS.get,
                key="scenario",
            )
        with seed_column:
            seed = st.number_input(
                "Semente",
                min_value=0,
                max_value=2_147_483_647,
                value=43,
                step=1,
                help="A mesma semente e quantidade reproduzem os mesmos produtos.",
                key="seed",
            )
        submitted = st.form_submit_button("Comparar algoritmos", type="primary")

    if submitted or "catalog_comparison" not in st.session_state:
        products = generate_products(quantity, scenario=scenario, seed=seed)
        st.session_state["catalog_comparison"] = {
            "quantity": quantity,
            "scenario": scenario,
            "seed": seed,
            "products": products,
            "results": compare_products(products),
        }

    comparison = st.session_state["catalog_comparison"]
    products = comparison["products"]
    insertion, merge = comparison["results"]
    original_positions = {product.identifier: index for index, product in enumerate(products, start=1)}

    st.caption(
        f"Resultado exibido: {comparison['quantity']} produtos · "
        f"Entrada {SCENARIO_LABELS[comparison['scenario']].lower()} · "
        f"Semente {comparison['seed']}"
    )

    with st.expander("Lista original"):
        st.dataframe(product_rows(products), hide_index=True, height=300, width="stretch")

    insertion_column, merge_column = st.columns(2)
    with insertion_column:
        render_result("Insertion Sort", insertion, original_positions)
    with merge_column:
        render_result("Merge Sort", merge, original_positions)

    st.subheader("Comparação do esforço de ordenação")
    st.bar_chart(
        [
            {"Algoritmo": "Insertion Sort", "Comparações": insertion.comparisons},
            {"Algoritmo": "Merge Sort", "Comparações": merge.comparisons},
        ],
        x="Algoritmo",
        y="Comparações",
        horizontal=True,
        height=180,
        color="#2563eb",
    )
    st.caption(
        "Cada comparação avalia dois preços. A contagem não representa tempo de execução."
    )

    with st.expander("Como conferir a estabilidade?"):
        st.write(
            "A ordenação é crescente e usa somente o preço. Quando há empate, "
            "o produto que aparecia primeiro na lista original permanece primeiro "
            "nos dois resultados. Confira essa propriedade pela coluna Ordem original."
        )
        st.write(
            "Insertion Sort costuma exigir menos comparações em entradas já ordenadas "
            "ou quase ordenadas. Merge Sort mantém crescimento da ordem de n log n "
            "mesmo quando a entrada está invertida."
        )

    render_benchmark()


if __name__ == "__main__":
    main()
