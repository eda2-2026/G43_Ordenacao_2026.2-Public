# Grupo 43 — Catálogo de Produtos

Trabalho 2 da disciplina de Estruturas de Dados 2, desenvolvido individualmente em Python.

O projeto implementa **Insertion Sort** e **Merge Sort** para ordenar produtos por preço e comparar a quantidade de comparações entre os algoritmos. A página Streamlit apresenta o tema e as características dos métodos.

## Funcionalidades

- Modelo de produto com identificador, nome e preço em centavos inteiros.
- Geração reproduzível de até 1.000 produtos fictícios a partir de uma semente.
- Quatro formatos de entrada: aleatória, ordenada, invertida e quase ordenada.
- Ordenação crescente por preço, com preservação da ordem relativa nos empates.
- Comparação dos algoritmos sobre a mesma entrada, sem modificar a lista original.
- Contagem opcional das comparações de preço realizadas por cada algoritmo.

## Algoritmos

| Algoritmo | Melhor caso | Caso médio | Pior caso | Memória auxiliar | Estável |
| --- | --- | --- | --- | --- | --- |
| Insertion Sort | Θ(n) | Θ(n²) | Θ(n²) | O(1)* | Sim |
| Merge Sort | Θ(n log n) | Θ(n log n) | Θ(n log n) | O(n) | Sim |

\* O Insertion Sort utiliza espaço constante para ordenar, além da cópia de O(n) elementos feita para preservar a entrada. As duas funções retornam uma nova lista.

Somente o preço é utilizado como chave de ordenação. O identificador distingue os produtos e não é usado como critério de desempate.

Uma comparação corresponde à avaliação entre duas chaves de preço. Verificações de índices e condições de laço não entram nessa contagem.

## Como executar

Requisito: Python 3.11 ou superior.

Execute os comandos a partir da pasta do projeto.

Crie um ambiente virtual:

```bash
python -m venv .venv
```

No Windows PowerShell, ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Instale a dependência e inicie a página de apresentação:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abra o endereço local informado pelo Streamlit no terminal.

Se preferir executar no PowerShell sem ativar o ambiente virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Usar a ordenação em Python

O núcleo de ordenação utiliza somente a biblioteca padrão. No terminal, execute `python` a partir da pasta do projeto e use:

```python
from services.generator import generate_products
from services.catalog import compare_products

products = generate_products(10, scenario="random", seed=43)
insertion, merge = compare_products(products)

for result in (insertion, merge):
    print(result.algorithm, "— comparações:", result.comparisons)
    for product in result.products:
        print(product.identifier, product.name, product.formatted_price)
```

Os formatos aceitos pelo gerador são:

| Valor de `scenario` | Formato |
| --- | --- |
| `random` | Preços gerados em ordem aleatória |
| `ordered` | Preços em ordem crescente |
| `reversed` | Preços em ordem decrescente |
| `nearly_ordered` | Lista crescente com uma troca entre vizinhos a cada 20 posições |

Para uma mesma quantidade e semente, os quatro formatos contêm os mesmos produtos. A preparação das entradas ordenadas utiliza o próprio Merge Sort.

Para ordenar com um algoritmo específico, sem contar comparações:

```python
from services.catalog import sort_products

result = sort_products(products, algorithm="merge", count_comparisons=False)
```

Nesse caso, `result.comparisons` é `None`. O gerador aceita quantidades entre 0 e 1.000; uma quantidade zero produz uma lista vazia.

## Estrutura

```text
algorithms/
  insertion_sort.py     Insertion Sort estável
  merge_sort.py         Merge Sort estável
  metrics.py            Contagem de comparações
models/
  product.py            Modelo e formatação de preços
services/
  generator.py          Geração dos quatro formatos de entrada
  catalog.py            Ordenação e comparação de produtos
app.py                  Página de apresentação Streamlit
requirements.txt        Dependência da interface
```
