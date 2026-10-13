"""Pagina inicial do comparador de ordenacao de produtos do grupo 43."""

import streamlit as st


def main() -> None:
    st.set_page_config(
        page_title="Catálogo de Produtos | Grupo 43",
        page_icon="🛒",
        layout="centered",
    )

    st.title("🛒 Catálogo de Produtos")
    st.caption("Estruturas de Dados 2 · Trabalho 2: Ordenação · Grupo 43")

    st.write(
        "Este projeto compara Insertion Sort e Merge Sort na ordenação "
        "de produtos por preço, usando a mesma lista de entrada para os dois algoritmos."
    )

    st.info(
        "A ordenação é crescente por preço. Produtos com o mesmo preço "
        "mantêm sua ordem relativa na entrada."
    )

    st.subheader("O que influencia a ordenação?")
    st.markdown(
        "- Como a quantidade de produtos afeta a ordenação.\n"
        "- Como listas aleatórias, ordenadas, invertidas e quase ordenadas "
        "afetam cada algoritmo.\n"
        "- Se produtos com o mesmo preço mantêm a ordem relativa da entrada."
    )

    st.subheader("Algoritmos")
    insertion, merge = st.columns(2)
    with insertion:
        st.markdown("**Insertion Sort**")
        st.write("Insere cada produto na posição correta da parte já ordenada da lista.")
    with merge:
        st.markdown("**Merge Sort**")
        st.write("Divide a lista em partes menores e intercala os resultados ordenados.")


if __name__ == "__main__":
    main()
