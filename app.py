"""Interface comparativa de ordenação de produtos do grupo 43."""

import streamlit as st

from models.product import Product
from services.catalog import SortResult, compare_products
from services.generator import generate_products

SCENARIO_LABELS = {
    "random": "Aleatória",
    "ordered": "Ordenada",
    "reversed": "Invertida",
    "nearly_ordered": "Quase ordenada",
}


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


if __name__ == "__main__":
    main()
