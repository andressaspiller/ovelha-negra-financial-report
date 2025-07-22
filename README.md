# Análise Financeira e Controle de Caixa

Este projeto contém scripts Python para análise de dados financeiros e controle de caixa, com foco em arrecadação. Os dados são provenientes de diversas planilhas do Google Sheets.

## Estrutura do Projeto

- `data/raw/`: Contém os arquivos CSV originais, conforme baixados das planilhas do Google Sheets.
- `data/cleaned/`: Contém os arquivos CSV após o processo de limpeza e estruturação dos dados.
- `scripts/`: Contém os scripts Python utilizados para limpeza, análise e geração de dashboards.
  - `data_cleaning_simple.py`: Script para limpeza e estruturação dos dados brutos.
  - `analyze_data.py`: Script para análise financeira e geração de insights.
  - `financial_analysis.py`: Script principal para a análise financeira e geração de resumos.
  - `create_excel_dashboards.py`: Script para gerar planilhas Excel com dashboards.
  - `create_advanced_dashboard.py`: Script para gerar dashboards interativos e análises de tendências.
- `reports/`: Contém os relatórios gerados, como o resumo financeiro e o relatório de insights.
- `dashboards/`: Contém os dashboards visuais gerados (imagens e arquivos HTML).

## Como Usar

1.  **Preparação dos Dados:** Certifique-se de que os arquivos CSV brutos estejam no diretório `data/raw/`.
2.  **Limpeza e Estruturação:** Execute o script `data_cleaning_simple.py` para limpar e estruturar os dados. Os arquivos limpos serão salvos em `data/cleaned/`.
    ```bash
    python3.11 scripts/data_cleaning_simple.py
    ```
3.  **Análise Financeira:** Execute o script `analyze_data.py` para realizar a análise financeira e gerar o resumo financeiro (`financial_summary.txt`) e o dashboard (`financial_dashboard.png`).
    ```bash
    python3.11 scripts/analyze_data.py
    ```
4.  **Dashboards Excel:** Execute o script `create_excel_dashboards.py` para gerar a planilha Excel com dashboards.
    ```bash
    python3.11 scripts/create_excel_dashboards.py
    ```
5.  **Dashboard Avançado e Insights:** Execute o script `create_advanced_dashboard.py` para gerar o dashboard interativo (`dashboard_interativo.html`), a análise de tendências (`trend_analysis.png`) e o relatório de insights (`insights_report.txt`).
    ```bash
    python3.11 scripts/create_advanced_dashboard.py
    ```

## Insights Principais

Os principais insights e o resumo financeiro podem ser encontrados em `reports/financial_summary.txt` e `reports/insights_report.txt`.

# Dashboard Financeiro Moderno com Streamlit

## 🚀 Dashboard Implementado

Este projeto agora inclui um dashboard moderno e robusto desenvolvido com Streamlit, oferecendo uma interface interativa e visualmente atrativa para análise dos dados financeiros.

## ✨ Principais Funcionalidades

### 📊 Métricas Principais
- **Receitas Totais**: Visualização consolidada de todas as fontes de receita
- **Despesas Totais**: Controle de gastos e saídas
- **Saldo Geral**: Situação financeira atual
- **Margem Líquida**: Indicador de performance financeira

### 📈 Visualizações Interativas
1. **Distribuição de Receitas por Fonte**: Gráfico de pizza mostrando a participação de cada fonte
2. **Comparação Receitas vs Despesas**: Gráfico de barras para análise comparativa
3. **Tendência Mensal**: Evolução das vendas de bombom e chup-chup ao longo dos meses
4. **Análise de Formas de Pagamento**: Distribuição dos métodos de pagamento utilizados

### 🎯 Insights Automáticos
- Identificação da principal fonte de receita
- Análise da situação financeira atual
- Recomendações estratégicas baseadas nos dados
- Alertas sobre tendências importantes

### 🔧 Funcionalidades Avançadas
- **Interface Responsiva**: Adaptável a diferentes tamanhos de tela
- **Sidebar Configurável**: Opções para personalizar a visualização
- **Atualização em Tempo Real**: Dados sempre atualizados
- **Design Moderno**: Interface limpa e profissional
- **Cores Personalizadas**: Esquema de cores atrativo e consistente

## 🚀 Como Executar o Dashboard

### Pré-requisitos
```bash
pip install streamlit pandas plotly matplotlib seaborn
```

### Execução Local
```bash
cd financial_analysis_project
streamlit run streamlit_dashboard.py
```

### Execução com Acesso Externo
```bash
streamlit run streamlit_dashboard.py --server.port 8501 --server.address 0.0.0.0
```

## 📱 Acesso ao Dashboard

O dashboard estará disponível em:
- **Local**: http://localhost:8501
- **Rede**: http://0.0.0.0:8501

## 🎨 Características do Design

### Paleta de Cores
- **Primária**: Gradiente azul-roxo (#667eea → #764ba2)
- **Receitas**: Verde (#2ECC71)
- **Despesas**: Vermelho (#E74C3C)
- **Neutro**: Cinza claro para fundos

### Layout
- **Header**: Título principal com gradiente
- **Métricas**: Cards coloridos com informações principais
- **Gráficos**: Dispostos em grid 2x2 para melhor visualização
- **Sidebar**: Configurações e informações adicionais

## 📊 Dados Processados

O dashboard processa automaticamente:
- Vendas de cachorro quente (portaria e campus)
- Arrecadações da obra do banheiro
- Movimentações da conta da casa
- Dados mensais de bombom e chup-chup
- Formas de pagamento utilizadas

## 🔍 Insights Gerados

### Análises Automáticas
1. **Fonte Principal de Receita**: Identifica qual atividade gera mais recursos
2. **Situação Financeira**: Avalia se o saldo é positivo ou negativo
3. **Tendências**: Analisa padrões nas vendas mensais
4. **Métodos de Pagamento**: Mostra preferências dos clientes

### Recomendações
- Manter foco na principal fonte de arrecadação
- Diversificar fontes de receita
- Controlar despesas rigorosamente
- Implementar campanhas adicionais quando necessário

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework principal para o dashboard
- **Plotly**: Gráficos interativos e modernos
- **Pandas**: Processamento e análise de dados
- **CSS Customizado**: Estilização avançada da interface

## 📈 Melhorias Implementadas

Comparado ao dashboard anterior:
- ✅ Interface muito mais moderna e atrativa
- ✅ Gráficos interativos com hover e zoom
- ✅ Layout responsivo e profissional
- ✅ Processamento automático de dados
- ✅ Insights gerados automaticamente
- ✅ Configurações personalizáveis
- ✅ Performance otimizada com cache
- ✅ Design consistente e intuitivo

## 🎯 Próximos Passos

Para futuras melhorias, considere:
1. Integração com banco de dados
2. Autenticação de usuários
3. Exportação de relatórios em PDF
4. Alertas automáticos por email
5. Previsões baseadas em machine learning
6. Dashboard mobile dedicado

---

**Desenvolvido com ❤️ usando Streamlit**