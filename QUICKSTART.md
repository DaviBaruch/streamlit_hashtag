# 🚀 Quick Start Guide

Comece a usar o Stock & Crypto Analysis Dashboard em menos de 5 minutos!

## 1. Instalação Rápida

```bash
# Navegue até o diretório do projeto
cd /home/ubuntu/stock_analysis_dashboard

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run main.py
```

## 2. Acesse a Aplicação

Abra seu navegador em: **http://localhost:8501**

## 3. Explore as Funcionalidades

### 📈 Página 1: Análise Individual
- Selecione um ativo (ex: AAPL, BTC-USD, ITUB4.SA)
- Configure o período (6 meses é o padrão recomendado)
- Ative indicadores técnicos (SMA, Bollinger)
- Visualize gráficos interativos e métricas

### ⚖️ Página 2: Comparação de Ativos
- Selecione 2-5 ativos para comparar
- Veja preços normalizados e retornos
- Analise a correlação entre ativos
- Compare performance visual

### 💼 Página 3: Portfólio
- Configure seu investimento inicial
- Adicione ativos e pesos (%)
- Simule o crescimento
- Analise contribuição de cada ativo

### 📊 Página 4: Indicadores Técnicos
- Escolha um ativo
- Ative múltiplos indicadores
- Veja sinais de compra/venda
- Interprete análises técnicas

## 4. Dicas Rápidas

✨ **Interação com Gráficos**
- Clique e arraste para fazer zoom
- Clique na legenda para ativar/desativar séries
- Passe o mouse para ver detalhes
- Use a ferramenta de download no canto superior direito

📊 **Seleção de Ativos**
- Use símbolos padrão: AAPL, MSFT, GOOGL, TSLA
- Ações brasileiras: ITUB4.SA, PETR4.SA, VALE3.SA
- Criptomoedas: BTC-USD, ETH-USD
- Índices: ^BVSP, ^GSPC, ^DJI

⏰ **Períodos Recomendados**
- **Curto prazo**: 1-3 meses
- **Médio prazo**: 6-12 meses
- **Longo prazo**: 5 anos

## 5. Exemplos Práticos

### Exemplo 1: Analisar Tesla (TSLA)
```
1. Vá para "Análise Individual"
2. Selecione "Ações US" → TSLA
3. Período: "6 Meses"
4. Tipo: "Linha"
5. Ative: "Mostrar Médias Móveis"
6. Visualize métricas como Volatilidade e Sharpe Ratio
```

### Exemplo 2: Comparar Gigantes de Tech
```
1. Vá para "Comparação de Ativos"
2. Tipo: "Ações US"
3. Selecione: AAPL, MSFT, GOOGL, NVDA
4. Período: "1 Ano"
5. Veja a correlação entre elas
```

### Exemplo 3: Simular Portfólio Diversificado
```
1. Vá para "Portfólio"
2. Investimento: $10,000
3. Ativo 1: AAPL (40%)
4. Ativo 2: BTC-USD (35%)
5. Ativo 3: ITUB4.SA (25%)
6. Clique "Simular Portfólio"
7. Análise retorno e risco
```

## 6. Solução de Problemas

### ❓ "Nenhum dado encontrado para XXX"
- ✅ Verifique a conexão com internet
- ✅ Verifique se o símbolo está correto
- ✅ Tente um período maior (ex: 1 ano em vez de 1 dia)

### ❓ Gráficos não carregam
- ✅ Recarregue a página (F5)
- ✅ Limpe o cache: `streamlit cache clear`
- ✅ Reinicie a aplicação

### ❓ Performance lenta
- ✅ Reduza o período de dados
- ✅ Use menos ativos na comparação
- ✅ Feche outras abas/aplicações

## 7. Atalhos Úteis

| Atalho | Ação |
|--------|------|
| `R` | Recarregar página |
| `C` | Limpar cache |
| `?` | Mostrar ajuda Streamlit |

## 8. Próximas Ações

Após explorar:
1. ✅ Customize as cores em `config.py`
2. ✅ Adicione seus ativos favoritos
3. ✅ Crie alertas (em desenvolvimento)
4. ✅ Exporte relatórios em PDF

## 9. Recursos

- 📚 [Documentação Completa](README.md)
- 🔗 [Streamlit Docs](https://docs.streamlit.io/)
- 📊 [yfinance GitHub](https://github.com/ranaroussi/yfinance)
- 📈 [Análise Técnica](https://www.investopedia.com/)

---

**Aproveite a análise! 📊💼**
