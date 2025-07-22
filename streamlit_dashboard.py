import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Dashboard Financeiro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carregar e processar todos os dados financeiros"""
    data_path = "data/cleaned/"
    
    # Dicionário para armazenar todos os dados
    datasets = {}
    
    # Lista de arquivos importantes
    important_files = [
        "Copyofcachorroquente-Vendaportaria_cleaned.csv",
        "CopyofOBRABANHEIROSETEMBRO25-Arrecadações_cleaned.csv",
        "Copyofcontadacasa-Entrada_saída2025-CONTANOVA(lofi)_cleaned.csv",
        "Copyofcontadacasa-Geral_cleaned.csv"
    ]
    
    # Dados mensais de bombom/chup-chup
    monthly_files = [
        "CopyofBombomechup-chup2025-Janeiro_cleaned.csv",
        "CopyofBombomechup-chup2025-Fevereiro_cleaned.csv",
        "CopyofBombomechup-chup2025-Março_cleaned.csv",
        "CopyofBombomechup-chup2025-Abril_cleaned.csv",
        "CopyofBombomechup-chup2025-Maio_cleaned.csv"
    ]
    
    # Carregar dados principais
    for file in important_files:
        try:
            if os.path.exists(os.path.join(data_path, file)):
                df = pd.read_csv(os.path.join(data_path, file))
                datasets[file.replace('_cleaned.csv', '')] = df
        except Exception as e:
            st.error(f"Erro ao carregar {file}: {e}")
    
    # Carregar dados mensais
    monthly_data = {}
    for file in monthly_files:
        try:
            if os.path.exists(os.path.join(data_path, file)):
                df = pd.read_csv(os.path.join(data_path, file))
                month = file.split('-')[2].replace('_cleaned.csv', '')
                monthly_data[month] = df
        except Exception as e:
            st.error(f"Erro ao carregar {file}: {e}")
    
    datasets['monthly_data'] = monthly_data
    
    return datasets

def process_financial_data(datasets):
    """Processar dados financeiros e calcular métricas"""
    metrics = {}
    
    # Processar vendas de cachorro quente
    if 'Copyofcachorroquente-Vendaportaria' in datasets:
        df_cachorro = datasets['Copyofcachorroquente-Vendaportaria']
        if 'Valor' in df_cachorro.columns:
            df_cachorro['Valor'] = pd.to_numeric(df_cachorro['Valor'], errors='coerce')
            metrics['total_cachorro_quente'] = df_cachorro['Valor'].sum()
            metrics['vendas_cachorro_count'] = len(df_cachorro)
        else:
            metrics['total_cachorro_quente'] = 0
            metrics['vendas_cachorro_count'] = 0
    
    # Processar arrecadações da obra do banheiro
    if 'CopyofOBRABANHEIROSETEMBRO25-Arrecadações' in datasets:
        df_obra = datasets['CopyofOBRABANHEIROSETEMBRO25-Arrecadações']
        valor_cols = [col for col in df_obra.columns if 'valor' in col.lower()]
        if valor_cols:
            df_obra[valor_cols[0]] = pd.to_numeric(df_obra[valor_cols[0]], errors='coerce')
            metrics['obra_banheiro_arrecadado'] = df_obra[valor_cols[0]].sum()
        else:
            metrics['obra_banheiro_arrecadado'] = 0
    
    # Processar dados da conta da casa
    if 'Copyofcontadacasa-Entrada_saída2025-CONTANOVA(lofi)' in datasets:
        df_conta = datasets['Copyofcontadacasa-Entrada_saída2025-CONTANOVA(lofi)']
        # Procurar por colunas de entrada e saída
        entrada_cols = [col for col in df_conta.columns if 'entrada' in col.lower()]
        saida_cols = [col for col in df_conta.columns if 'saída' in col.lower() or 'saida' in col.lower()]
        
        total_entradas = 0
        total_saidas = 0
        
        for col in entrada_cols:
            df_conta[col] = pd.to_numeric(df_conta[col], errors='coerce')
            total_entradas += df_conta[col].sum()
        
        for col in saida_cols:
            df_conta[col] = pd.to_numeric(df_conta[col], errors='coerce')
            total_saidas += df_conta[col].sum()
        
        metrics['conta_casa_entradas'] = total_entradas
        metrics['conta_casa_saidas'] = total_saidas
    
    # Processar dados mensais
    if 'monthly_data' in datasets:
        monthly_totals = {}
        for month, df in datasets['monthly_data'].items():
            total = 0
            for col in df.columns:
                if 'valor' in col.lower() and 'obtido' in col.lower():
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    total += df[col].sum()
            monthly_totals[month] = total
        metrics['monthly_bombom'] = monthly_totals
    
    # Calcular totais
    metrics['total_receitas'] = (
        metrics.get('total_cachorro_quente', 0) + 
        metrics.get('obra_banheiro_arrecadado', 0) + 
        metrics.get('conta_casa_entradas', 0)
    )
    
    metrics['total_despesas'] = metrics.get('conta_casa_saidas', 0)
    metrics['saldo_geral'] = metrics['total_receitas'] - metrics['total_despesas']
    
    return metrics

def create_overview_metrics(metrics):
    """Criar métricas de visão geral"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Receitas Totais</h3>
            <h2>R$ {:.2f}</h2>
        </div>
        """.format(metrics.get('total_receitas', 0)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>💸 Despesas Totais</h3>
            <h2>R$ {:.2f}</h2>
        </div>
        """.format(metrics.get('total_despesas', 0)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Saldo Geral</h3>
            <h2>R$ {:.2f}</h2>
        </div>
        """.format(metrics.get('saldo_geral', 0)), unsafe_allow_html=True)
    
    with col4:
        margem = (metrics.get('saldo_geral', 0) / metrics.get('total_receitas', 1)) * 100 if metrics.get('total_receitas', 0) > 0 else 0
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Margem Líquida</h3>
            <h2>{:.1f}%</h2>
        </div>
        """.format(margem), unsafe_allow_html=True)

def create_revenue_breakdown(metrics):
    """Criar gráfico de distribuição de receitas"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🎯 Distribuição de Receitas por Fonte")
    
    # Dados para o gráfico de pizza
    labels = ['Cachorro Quente', 'Obra Banheiro', 'Conta da Casa']
    values = [
        metrics.get('total_cachorro_quente', 0),
        metrics.get('obra_banheiro_arrecadado', 0),
        metrics.get('conta_casa_entradas', 0)
    ]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=colors,
        textinfo='label+percent+value',
        textfont_size=12,
        hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:.2f}<br>Percentual: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Distribuição de Receitas",
        font=dict(size=14),
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def create_monthly_trend(metrics):
    """Criar gráfico de tendência mensal"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📈 Tendência Mensal - Bombom e Chup-chup")
    
    if 'monthly_bombom' in metrics:
        monthly_data = metrics['monthly_bombom']
        months = list(monthly_data.keys())
        values = list(monthly_data.values())
        
        # Ordenar por mês
        month_order = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio']
        sorted_data = [(month, monthly_data.get(month, 0)) for month in month_order if month in monthly_data]
        
        if sorted_data:
            months, values = zip(*sorted_data)
            
            fig = go.Figure()
            
            # Linha principal
            fig.add_trace(go.Scatter(
                x=months,
                y=values,
                mode='lines+markers',
                name='Vendas Mensais',
                line=dict(color='#667eea', width=3),
                marker=dict(size=10, color='#667eea'),
                hovertemplate='<b>%{x}</b><br>Valor: R$ %{y:.2f}<extra></extra>'
            ))
            
            # Área preenchida
            fig.add_trace(go.Scatter(
                x=months,
                y=values,
                fill='tonexty',
                mode='none',
                fillcolor='rgba(102, 126, 234, 0.2)',
                showlegend=False
            ))
            
            fig.update_layout(
                title="Evolução das Vendas de Bombom e Chup-chup",
                xaxis_title="Mês",
                yaxis_title="Valor (R$)",
                font=dict(size=12),
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Dados mensais não disponíveis")
    else:
        st.info("Dados mensais não encontrados")
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_comparison_chart(metrics):
    """Criar gráfico de comparação receitas vs despesas"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("⚖️ Receitas vs Despesas")
    
    categories = ['Receitas', 'Despesas']
    values = [metrics.get('total_receitas', 0), metrics.get('total_despesas', 0)]
    colors = ['#2ECC71', '#E74C3C']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f'R$ {v:.2f}' for v in values],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Valor: R$ %{y:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Comparação Receitas vs Despesas",
        yaxis_title="Valor (R$)",
        font=dict(size=12),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def create_payment_methods_analysis(datasets):
    """Analisar formas de pagamento"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💳 Análise de Formas de Pagamento")
    
    if 'Copyofcachorroquente-Vendaportaria' in datasets:
        df = datasets['Copyofcachorroquente-Vendaportaria']
        
        # Procurar coluna de forma de pagamento
        payment_col = None
        for col in df.columns:
            if 'forma' in col.lower() and 'pagamento' in col.lower():
                payment_col = col
                break
        
        if payment_col and 'Valor' in df.columns:
            df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
            payment_summary = df.groupby(payment_col)['Valor'].agg(['sum', 'count']).reset_index()
            payment_summary.columns = ['Forma de Pagamento', 'Valor Total', 'Quantidade']
            
            # Gráfico de pizza para formas de pagamento
            fig = go.Figure(data=[go.Pie(
                labels=payment_summary['Forma de Pagamento'],
                values=payment_summary['Valor Total'],
                hole=0.3,
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:.2f}<br>Transações: %{customdata}<br>Percentual: %{percent}<extra></extra>',
                customdata=payment_summary['Quantidade']
            )])
            
            fig.update_layout(
                title="Distribuição por Forma de Pagamento",
                font=dict(size=12),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada
            st.subheader("📋 Detalhamento por Forma de Pagamento")
            payment_summary['Valor Total'] = payment_summary['Valor Total'].apply(lambda x: f'R$ {x:.2f}')
            st.dataframe(payment_summary, use_container_width=True)
        else:
            st.info("Dados de forma de pagamento não encontrados")
    else:
        st.info("Dados de vendas não disponíveis")
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_insights_section(metrics):
    """Criar seção de insights"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💡 Insights e Recomendações")
    
    insights = []
    
    # Análise da principal fonte de receita
    total_receitas = metrics.get('total_receitas', 0)
    obra_banheiro = metrics.get('obra_banheiro_arrecadado', 0)
    cachorro_quente = metrics.get('total_cachorro_quente', 0)
    conta_casa = metrics.get('conta_casa_entradas', 0)
    
    if total_receitas > 0:
        if obra_banheiro > cachorro_quente and obra_banheiro > conta_casa:
            insights.append(f"🎯 **Principal fonte de receita**: Obra Banheiro ({(obra_banheiro/total_receitas)*100:.1f}% do total)")
        elif cachorro_quente > conta_casa:
            insights.append(f"🎯 **Principal fonte de receita**: Cachorro Quente ({(cachorro_quente/total_receitas)*100:.1f}% do total)")
        else:
            insights.append(f"🎯 **Principal fonte de receita**: Conta da Casa ({(conta_casa/total_receitas)*100:.1f}% do total)")
    
    # Análise da situação financeira
    saldo_geral = metrics.get('saldo_geral', 0)
    if saldo_geral > 0:
        insights.append(f"✅ **Situação financeira positiva** com saldo de R$ {saldo_geral:.2f}")
    else:
        insights.append(f"⚠️ **Atenção**: Situação financeira negativa com déficit de R$ {abs(saldo_geral):.2f}")
    
    # Recomendações
    insights.append("📈 **Recomendações estratégicas**:")
    insights.append("• Manter foco na principal fonte de arrecadação")
    insights.append("• Diversificar fontes de receita para reduzir riscos")
    insights.append("• Implementar controle rigoroso de despesas")
    insights.append("• Considerar campanhas de arrecadação adicionais")
    insights.append("• Monitorar tendências mensais para planejamento")
    
    for insight in insights:
        st.markdown(insight)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Função principal do dashboard"""
    # Cabeçalho
    st.markdown('<h1 class="main-header">💰 Dashboard Financeiro Avançado</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.header("🔧 Configurações")
        
        # Filtros e opções
        show_details = st.checkbox("Mostrar detalhes avançados", value=True)
        auto_refresh = st.checkbox("Atualização automática", value=False)
        
        if auto_refresh:
            st.info("Dashboard será atualizado automaticamente")
        
        st.markdown("---")
        st.markdown("**📊 Sobre este Dashboard**")
        st.markdown("Este dashboard apresenta uma análise completa dos dados financeiros, incluindo receitas, despesas e tendências.")
        
        st.markdown("---")
        st.markdown(f"**🕒 Última atualização**: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Carregar dados
    with st.spinner("Carregando dados financeiros..."):
        datasets = load_data()
        metrics = process_financial_data(datasets)
    
    # Métricas principais
    create_overview_metrics(metrics)
    
    # Layout em colunas para gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        create_revenue_breakdown(metrics)
        create_comparison_chart(metrics)
    
    with col2:
        create_monthly_trend(metrics)
        create_payment_methods_analysis(datasets)
    
    # Seção de insights
    create_insights_section(metrics)
    
    # Seção de detalhes (se habilitada)
    if show_details:
        st.markdown("---")
        st.subheader("📋 Dados Detalhados")
        
        # Exibir métricas detalhadas
        with st.expander("Ver métricas detalhadas"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Vendas Cachorro Quente", f"R$ {metrics.get('total_cachorro_quente', 0):.2f}")
                st.metric("Arrecadação Obra Banheiro", f"R$ {metrics.get('obra_banheiro_arrecadado', 0):.2f}")
            
            with col2:
                st.metric("Entradas Conta Casa", f"R$ {metrics.get('conta_casa_entradas', 0):.2f}")
                st.metric("Saídas Conta Casa", f"R$ {metrics.get('conta_casa_saidas', 0):.2f}")
    
    # Rodapé
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8rem;'>"
        "Dashboard Financeiro - Desenvolvido com Streamlit | "
        f"Dados atualizados em {datetime.now().strftime('%d/%m/%Y')}"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

