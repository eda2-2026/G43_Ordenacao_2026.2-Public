# Grupo 43 — Catálogo de Produtos

Trabalho 2 da disciplina de Estruturas de Dados 2, desenvolvido individualmente em Python.

O projeto compara **Insertion Sort** e **Merge Sort**, implementados manualmente, na ordenação crescente de produtos por preço. A interface será construída em uma única página com Streamlit.

## Estado atual

Esta primeira etapa entrega a estrutura do projeto, a definição do escopo, as dependências e uma página inicial executável. Os algoritmos, a geração de produtos, os testes e o benchmark ainda serão implementados.

## Objetivo

Investigar como o tamanho e a organização da entrada afetam o desempenho dos algoritmos, comparando o tempo de ordenação e a quantidade de comparações. Também será verificada a preservação da ordem relativa dos produtos com preços iguais.

## Escopo

- Cada produto terá identificador, nome e preço em centavos inteiros.
- A ordenação será crescente, utilizando somente o preço como chave.
- O usuário poderá gerar entre 10 e 1.000 produtos fictícios.
- Haverá quatro formatos de entrada: aleatória, ordenada, invertida e quase ordenada.
- Ambos os algoritmos receberão cópias da mesma entrada.
- A interface exibirá a lista original, os resultados e as métricas.
- A geração utilizará uma semente para permitir a reprodução dos cenários.

Esta versão não inclui banco de dados, autenticação, APIs, importação de arquivos ou animações da execução.

## Algoritmos planejados

| Algoritmo | Melhor caso | Caso médio | Pior caso | Estabilidade prevista |
| --- | --- | --- | --- | --- |
| Insertion Sort | Θ(n) | Θ(n²) | Θ(n²) | Estável |
| Merge Sort | Θ(n log n) | Θ(n log n) | Θ(n log n) | Estável |

As implementações preservarão a ordem relativa nos empates. O identificador servirá para distinguir os produtos, sem funcionar como critério de desempate.

## Como executar

Requisito: Python 3.11 ou superior. A primeira etapa foi verificada com Python 3.14.3 e Streamlit 1.62.0.

Execute os comandos a partir da pasta `G43_Ordenacao_2026.2`.

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

Abra o endereço local informado pelo Streamlit no terminal. Nesta etapa, a aplicação apresenta o tema e o planejamento do trabalho.

Se preferir executar no PowerShell sem ativar o ambiente virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Estrutura

```text
G43_Ordenacao_2026.2/
├── algorithms/         # Implementações manuais dos algoritmos
├── models/             # Modelo de produto
├── services/           # Geração de entradas e integração dos algoritmos
├── tests/              # Testes de corretude e estabilidade
├── benchmark/          # Experimentos de desempenho
├── app.py              # Página da aplicação Streamlit
├── requirements.txt    # Dependência da interface
├── .gitignore
└── README.md
```

As pastas estão reservadas para as próximas etapas e ainda não contêm as funcionalidades descritas.

## Plano de desenvolvimento e commits

1. **`chore: iniciar estrutura do grupo 43`** — Estrutura, página inicial, dependência e documentação do escopo.
2. **`feat: implementar ordenacao de produtos`** — Modelo, geração dos quatro formatos de entrada, Insertion Sort e Merge Sort.
3. **`test: validar algoritmos de ordenacao`** — Testes com listas vazias, unitárias, empates e diferentes formatos de entrada; preservação dos produtos e da entrada original.
4. **`feat: adicionar interface comparativa`** — Controles de geração, visualização das listas e quantidade de comparações.
5. **`feat: adicionar benchmark e documentar resultados`** — Medição dos tempos, apresentação dos resultados e documentação final.

Cada commit será feito quando sua etapa estiver implementada e verificada.

## Metodologia prevista

O benchmark comparará entradas de 100, 500 e 1.000 produtos, nos quatro formatos, com cinco repetições e registro da mediana. A geração dos dados e a renderização da interface ficarão fora do tempo medido.

A contagem de comparações será executada separadamente das medições de tempo para reduzir a interferência da instrumentação. `sorted()` será utilizado como referência nos testes, sem substituir as implementações manuais na aplicação.

Não há resultados de desempenho nesta etapa.

## Critérios de conclusão

- Os dois algoritmos produzem preços em ordem crescente, sem perder ou duplicar produtos.
- A entrada original permanece intacta após a ordenação.
- Produtos com preços iguais preservam a ordem relativa da entrada.
- Os casos extremos e os quatro formatos de entrada são validados por testes.
- A aplicação permite comparar os dois algoritmos sobre os mesmos dados.
- O README final registra a execução, a metodologia, os resultados medidos e suas limitações.
