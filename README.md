# Grupo 43 — Catálogo de Produtos

Trabalho 2 da disciplina de Estruturas de Dados 2, desenvolvido individualmente em Python.

O projeto implementa **Insertion Sort** e **Merge Sort** para ordenar produtos por preço e comparar a quantidade de comparações e o tempo de ordenação. A interface Streamlit permite gerar as entradas e visualizar os resultados lado a lado.

## Funcionalidades

- Modelo de produto com identificador, nome e preço em centavos inteiros.
- Geração reproduzível de até 1.000 produtos fictícios a partir de uma semente.
- Quatro formatos de entrada: aleatória, ordenada, invertida e quase ordenada.
- Ordenação crescente por preço, com preservação da ordem relativa nos empates.
- Comparação dos algoritmos sobre a mesma entrada, sem modificar a lista original.
- Contagem opcional das comparações de preço realizadas por cada algoritmo.
- Interface com controles de quantidade, formato e semente, tabelas e gráfico de comparações.
- Benchmark com medições repetidas, mediana dos tempos, gráfico e exportação em CSV.

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

Instale a dependência e inicie a aplicação:

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

## Usar a interface

1. Escolha entre 10 e 1.000 produtos, o formato da entrada e uma semente.
2. Clique em **Comparar algoritmos** para atualizar os resultados.
3. Abra **Lista original** para consultar a entrada e compare as duas tabelas ordenadas.

A página apresenta uma comparação inicial com 20 produtos. O resumo acima das tabelas identifica a configuração dos resultados exibidos. Alterações nos controles são aplicadas ao clicar no botão.

As métricas e o gráfico mostram comparações de preço, não tempo de execução. A coluna **Ordem original** identifica a posição do produto na entrada e permite verificar a preservação dos empates.

Na seção **Benchmark de desempenho**, escolha a quantidade de repetições e a semente, e clique em **Executar benchmark**. A tabela contém os dois algoritmos para 100, 500 e 1.000 produtos nos quatro formatos de entrada. Selecione um formato para consultar o gráfico de tempos e use **Baixar resultados em CSV** para exportar as medições. O benchmark é independente dos controles do catálogo.

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

## Executar o benchmark no terminal

O benchmark utiliza somente a biblioteca padrão do Python. Para executar os três tamanhos com cinco repetições e semente 43:

```bash
python -m benchmark
```

Para salvar os resultados e as amostras individuais em CSV:

```bash
python -m benchmark --csv benchmark/results.csv
```

É possível configurar os tamanhos, as repetições e a semente:

```bash
python -m benchmark --sizes 100 500 1000 --repetitions 7 --seed 43
```

O comando aceita tamanhos de 1 a 1.000, sem duplicatas, e de 1 a 100 repetições. A interface limita as repetições a 15.

## Metodologia do benchmark

- Os algoritmos recebem a mesma lista de produtos para cada tamanho e formato.
- Cada algoritmo realiza uma execução de aquecimento antes das medições.
- O tempo é medido com `time.perf_counter_ns()` e convertido para milissegundos.
- O intervalo medido inclui a função de ordenação e a cópia da entrada feita por ela.
- A geração dos produtos, a interface, a liberação da lista resultante e a contagem de comparações ficam fora desse intervalo.
- A contagem de comparações é obtida em uma execução separada, sobre a mesma entrada.
- A ordem de execução dos algoritmos alterna entre as repetições.
- O resultado é a mediana dos tempos. O CSV também registra todas as amostras individuais.

A semente reproduz os dados, mas não os tempos. Carga do sistema, ambiente de execução e características do computador afetam as medições. O experimento compara estas implementações em Python; os tempos, isoladamente, não demonstram a complexidade assintótica.

## Resultados medidos

Execução em **12/10/2026**, com **CPython 3.14.3**, **Windows AMD64**, semente **43**, **cinco repetições** e um aquecimento por algoritmo. Os resultados foram coletados no ambiente automatizado local de desenvolvimento.

Os valores abaixo são medianas em milissegundos. As amostras e as contagens completas estão em [benchmark/results.csv](benchmark/results.csv).

| Produtos | Entrada | Insertion Sort (ms) | Merge Sort (ms) |
| --- | --- | ---: | ---: |
| 100 | Aleatória | 0.5058 | 0.3324 |
| 100 | Ordenada | 0.0321 | 0.2474 |
| 100 | Invertida | 0.6474 | 0.1848 |
| 100 | Quase ordenada | 0.0199 | 0.1569 |
| 500 | Aleatória | 11.5503 | 1.9590 |
| 500 | Ordenada | 0.2388 | 2.2634 |
| 500 | Invertida | 23.3338 | 1.8068 |
| 500 | Quase ordenada | 0.2049 | 1.7736 |
| 1000 | Aleatória | 57.7413 | 6.1516 |
| 1000 | Ordenada | 0.3105 | 2.5049 |
| 1000 | Invertida | 171.6617 | 5.2248 |
| 1000 | Quase ordenada | 0.3675 | 3.5304 |

Nesta execução, Insertion Sort apresentou as menores medianas nas entradas ordenadas e quase ordenadas. Merge Sort apresentou as menores medianas nas entradas aleatórias e invertidas, para os três tamanhos.

Com 1.000 produtos, Insertion Sort realizou **999 comparações** na entrada ordenada e **499.500** na invertida. Merge Sort realizou **4.932** e **5.048**, respectivamente. Essas contagens ajudam a explicar a influência do formato da entrada. Diferenças pequenas de tempo podem sofrer influência do ruído do sistema, mesmo usando a mediana.

## Testes

Instale as dependências de desenvolvimento no ambiente virtual:

```bash
python -m pip install -r requirements-dev.txt
```

Execute a suíte a partir da pasta do projeto:

```bash
python -m pytest -q
```

Os testes verificam a corretude dos algoritmos usando `sorted()` como referência, a estabilidade nos empates, a preservação da entrada e a contagem de comparações. Também cobrem a geração reproduzível dos quatro formatos, entradas de até 1.000 produtos, validações e formatação monetária.

Cada algoritmo é validado sobre as 1.093 combinações de listas de até seis elementos com três preços possíveis, incluindo entradas vazias e empates.

Os testes da interface utilizam o Streamlit AppTest para validar o carregamento inicial, os quatro formatos de entrada, a atualização das tabelas e das métricas, e a manutenção dos resultados até o envio do formulário.

Os testes do benchmark verificam a cobertura dos cenários, o cálculo da mediana com relógio controlado, a alternância de execução, a separação entre medição e contagem de comparações, a exportação CSV e a execução pela interface.

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
benchmark/
  __main__.py           Execução pelo terminal
  runner.py             Medições e exportação CSV
  results.csv           Resultados e amostras da execução documentada
tests/
  test_app.py           Integração da interface Streamlit
  test_algorithms.py    Corretude, estabilidade e contagem de comparações
  test_benchmark.py     Metodologia, métricas e exportação
  test_catalog.py       Integração e preservação dos produtos
  test_generator.py     Formatos de entrada e reprodução dos dados
  test_product.py       Validação e formatação monetária
app.py                  Interface comparativa Streamlit
requirements.txt        Dependência da interface
requirements-dev.txt    Dependências de desenvolvimento
```
