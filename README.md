# 📊 Stock & Crypto Analysis Dashboard

Um dashboard profissional e interativo para análise de ações e criptomoedas, desenvolvido com Streamlit, Plotly e yfinance.

## ✨ Características Principais

### 1. **Análise Individual de Ativos** 📈
- Visualização interativa de preços com múltiplos tipos de gráficos
- Indicadores técnicos (SMA, Bollinger Bands)
- Métricas financeiras completas (Preço, Variação, Volatilidade, Sharpe Ratio)
- Análise de volume e retorno cumulativo
- Download de dados em CSV

### 2. **Comparação de Ativos** ⚖️
- Compare preços normalizados (base 100) de múltiplos ativos
- Análise de retorno cumulativo em %
- Matriz de correlação interativa (heatmap)
- Comparação de performance visual
- Suporta até 10 ativos simultâneos

### 3. **Simulador de Portfólio** 💼
- Crie e simule alocações de portfólio
- Visualize crescimento do investimento
- Análise de contribuição por ativo
- Cálculo de retorno ponderado
- Exportar simulação em CSV

### 4. **Indicadores Técnicos Avançados** 📊
- **SMA (20, 50, 200 dias)**: Médias móveis simples
- **Bollinger Bands**: Análise de volatilidade
- **RSI (14)**: Índice de força relativa
- **MACD**: Convergência/divergência de médias
- Sinais de compra/venda automáticos

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Passos de Instalação

1. **Clone ou copie o projeto:**
```bash
cd /home/ubuntu/stock_analysis_dashboard
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação:**
```bash
streamlit run main.py
```

4. **Acesse no navegador:**
```
http://localhost:8501
```

## 📦 Estrutura do Projeto

```
stock_analysis_dashboard/
├── main.py                      # Arquivo principal (página inicial)
├── config.py                    # Configurações globais
├── requirements.txt             # Dependências
├── README.md                    # Este arquivo
│
├── utils/                       # Módulo de utilitários
│   ├── __init__.py
│   ├── data_fetcher.py         # Download de dados (yfinance)
│   ├── indicators.py           # Indicadores técnicos
│   ├── metrics.py              # Cálculos de métricas
│   └── portfolio.py            # Análise de portfólio
│
└── pages/                       # Páginas Streamlit multi-página
    ├── __init__.py
    ├── 01_analise_individual.py  # Análise de um ativo
    ├── 02_comparacao_ativos.py   # Comparação de múltiplos ativos
    ├── 03_portfolio.py           # Simulador de portfólio
    └── 04_indicadores.py         # Análise de indicadores técnicos
```

## 🔧 Dependências Principais

| Pacote | Versão | Uso |
|--------|--------|-----|
| `streamlit` | 1.31.1 | Framework web |
| `yfinance` | 0.2.32 | API de dados financeiros |
| `pandas` | 2.1.3 | Manipulação de dados |
| `plotly` | 5.18.0 | Gráficos interativos |
| `numpy` | >=1.26.0 | Cálculos numéricos |

## 📊 Ativos Suportados

### Ações Brasileiras
- ITUB4.SA (Itaú)
- PETR4.SA (Petrobras)
- MGLU3.SA (Magazine Luiza)
- VALE3.SA (Vale)
- GGBR4.SA (Gerdau)
- BBDC4.SA (Bradesco)
- ABEV3.SA (Ambev)

### Ações Americanas
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Google)
- AMZN (Amazon)
- TSLA (Tesla)
- NVDA (Nvidia)
- META (Meta Platforms)

### Criptomoedas
- BTC-USD (Bitcoin)
- ETH-USD (Ethereum)
- BNB-USD (Binance Coin)
- ADA-USD (Cardano)
- SOL-USD (Solana)

### Índices
- ^BVSP (Ibovespa)
- ^GSPC (S&P 500)
- ^DJI (Dow Jones)
- ^IXIC (NASDAQ)

## 📈 Indicadores Técnicos Explicados

### SMA (Simple Moving Average)
Suaviza dados de preço para identificar tendências. Use períodos diferentes:
- **20 dias**: Análise de curto prazo
- **50 dias**: Análise de médio prazo
- **200 dias**: Análise de longo prazo

### Bollinger Bands
Mostra volatilidade do ativo:
- Preço perto da banda superior → Sobrecomprado
- Preço perto da banda inferior → Sobrevendido
- Padrão: 20 dias, 2 desvios padrão

### RSI (Relative Strength Index)
Mede força relativa (0-100):
- **RSI > 70**: Sobrecomprado (sinal de venda)
- **RSI < 30**: Sobrevendido (sinal de compra)
- **RSI ≈ 50**: Mercado neutro

### MACD (Moving Average Convergence Divergence)
Identifica mudanças de tendência:
- MACD cruza acima da Signal → Sinal de Compra
- MACD cruza abaixo da Signal → Sinal de Venda

## 💡 Como Usar

### Análise Individual
1. Acesse a página **"Análise Individual"**
2. Selecione um ativo (tipo e símbolo)
3. Configure o período (pré-definido ou personalizado)
4. Escolha tipo de gráfico (Linha ou Candlestick)
5. Ative indicadores conforme desejado
6. Visualize métricas e gráficos interativos

### Comparação de Ativos
1. Acesse a página **"Comparação de Ativos"**
2. Selecione 2 ou mais ativos
3. Configure o período
4. Visualize gráficos de comparação
5. Analise a matriz de correlação

### Simulador de Portfólio
1. Acesse a página **"Portfólio"**
2. Configure investimento inicial
3. Adicione ativos com seus pesos (%)
4. Clique em "Simular Portfólio"
5. Analise crescimento e contribuições
6. Exporte resultados em CSV

### Análise de Indicadores
1. Acesse a página **"Indicadores Técnicos"**
2. Selecione um ativo
3. Escolha indicadores desejados
4. Visualize gráficos com sinais
5. Interprete sinais de compra/venda

## 🎨 Características de UX/UI

- ✅ **Tema Escuro Profissional**: Cores consistentes e elegantes
- ✅ **Gráficos Interativos**: Zoom, pan, hover detalhado com Plotly
- ✅ **Layout Responsivo**: Adapta-se a diferentes tamanhos de tela
- ✅ **Cache de Dados**: Otimizado para performance
- ✅ **Tratamento de Erros**: Mensagens claras e informativas
- ✅ **Download de Dados**: Exporte análises em CSV

## 🔍 Validação de Dados

- ✅ Validação automática de tickers
- ✅ Tratamento robusto de erros de conexão
- ✅ Limite de dados (máximo 5 anos por padrão)
- ✅ Cache automático por 1 hora
- ✅ Logging de operações para debugging

## 🛠️ Boas Práticas Implementadas

### Código
- ✅ **Type Hints**: Todas as funções com type hints
- ✅ **Docstrings**: Documentação descritiva
- ✅ **Modularização**: Código organizado e reutilizável
- ✅ **Cache**: @st.cache_data para performance
- ✅ **Logging**: Rastreamento de operações

### Performance
- ✅ Cache de 1 hora para dados
- ✅ Lazy loading de indicadores
- ✅ Limite de dados para evitar sobrecarga
- ✅ Otimização de cálculos

### Segurança
- ✅ Validação de inputs
- ✅ Tratamento de exceções
- ✅ Verificação de tickers válidos

## 📝 Exemplos de Uso

### Exemplo 1: Analisar uma ação individual
```python
# Dados históricos de AAPL
# - Período: 6 meses
# - Gráfico: Candlestick
# - Indicadores: SMA 20/50, Bollinger Bands
# - Métricas: Preço, Volatilidade, Sharpe Ratio
```

### Exemplo 2: Comparar ações
```python
# Comparar AAPL, MSFT, GOOGL
# - Preços normalizados (base 100)
# - Retorno acumulado (%)
# - Correlação entre ativos
```

### Exemplo 3: Simular portfólio
```python
# Portfólio com:
# - 40% AAPL
# - 35% MSFT
# - 25% GOOGL
# Período: 1 ano
# Investimento inicial: $10,000
```

## ⚠️ Limitações e Considerações

1. **Dados em Tempo Real**: Os dados têm até 1 dia de atraso
2. **Conexão Internet**: Requer conexão para baixar dados
3. **Taxa Livre de Risco**: Hardcoded em 2% a.a. para Sharpe Ratio
4. **Alertas**: Não há sistema de alertas automáticos
5. **Histórico**: Cache de 1 hora (sem histórico persistente)

## 🚀 Melhorias Futuras

- [ ] Sistema de alertas por email
- [ ] Histórico persistente de simulações
- [ ] Análise de sentimento de notícias
- [ ] Backtesting de estratégias
- [ ] Integração com APIs de corretoras
- [ ] Análise de opções
- [ ] Exportação em múltiplos formatos
- [ ] Dashboard de risco

## 📚 Recursos Adicionais

- [Documentação Streamlit](https://docs.streamlit.io/)
- [yfinance Documentação](https://github.com/ranaroussi/yfinance)
- [Plotly Documentação](https://plotly.com/python/)
- [Análise Técnica](https://www.investopedia.com/technical-analysis/)

## 👨‍💻 Desenvolvido Por

Projeto desenvolvido como exemplo de **dashboard profissional** para análise financeira.

### Tecnologias Utilizadas
- Python 3.8+
- Streamlit (Framework Web)
- Plotly (Visualização)
- yfinance (Dados)
- Pandas (Análise)

## 📄 Licença

Este projeto é fornecido como exemplo educacional.

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências foram instaladas
2. Verifique sua conexão com a internet
3. Limpe o cache: `streamlit cache clear`
4. Reinicie a aplicação

---

**Desenvolvido com ❤️ para análise profissional de mercados financeiros**
