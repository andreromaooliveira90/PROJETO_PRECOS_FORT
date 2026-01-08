# 🛒 Monitoramento de Preços: Atacarejo Inteligente

Este projeto realiza o monitoramento automatizado de preços de itens essenciais e de lazer em um supermercado atacadista de Florianópolis/SC. O objetivo é criar uma base de dados histórica para análise de sazonalidade, correlação de preços e identificação dos melhores dias para compra.

## 🚀 Objetivo
Extrair diariamente os preços de categorias estratégicas (Cesta Básica, Hortifrúti, Churrasco) através da API interna da plataforma VTEX, permitindo análises futuras de Ciência de Dados e Machine Learning.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.9+
* **Bibliotecas:** Pandas (Tratamento de dados), Requests (Coleta), OS/Sys (Manipulação de arquivos).
* **Automação:** GitHub Actions (Execução agendada).
* **Armazenamento:** Arquivos CSV (Série Temporal).

## 📁 Estrutura do Projeto
PROJETO_PRECOS_FORT/
├── .github/workflows/   # Configuração da automação diária
├── config/              # Dicionário de URLs e IDs de produtos
├── data/
│   ├── raw/             # Dados brutos coletados (Histórico CSV)
│   └── processed/       # Dados limpos para análise
├── notebooks/           # Análises exploratórias (Jupyter)
└── scripts/             # Scripts principais de coleta e utilitários

## 📊 Categorias Monitoradas
* **Cesta Básica:** Arroz, Feijão, Óleo, Café, Leite.
* **Hortifrúti:** Batata, Cebola, Ovos.
* **Churrasco:** Contrafilé, Frango, Cerveja e Carvão.

## ⚙️ Como Executar
1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Execute o coletor: `python scripts/fort_atacadista.py`.

## 📉 Análise Econômica e Insights (Business Intelligence)
Como economista, este pipeline foi desenhado para permitir análises de:
* **Índice de Preços Personalizado:** Criação de um índice de inflação próprio para itens de alto consumo (ex: Cesta Básica vs. Churrasco).
* **Elasticidade e Sazonalidade:** Identificação de ciclos de oferta (ex: promoções de hortifrúti no meio da semana) e o impacto no custo de aquisição.
* **Otimização de Orçamento:** Algoritmo para sugerir o "dia ideal de compra" com base na série histórica capturada pelo pipeline.

## 📈 Próximos Passos
- [ ] Criar dashboard de comparação de preços entre dias da semana.
- [ ] Calcular a volatilidade de cada categoria.
- [ ] Implementar modelo de regressão para prever o preço do final de semana.
