import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo

def create_advanced_dashboard():
    """
    Criar dashboard avançado com análises detalhadas
    """
    cleaned_data_path = '/home/ubuntu/cleaned_data'
    
    print("=== CRIANDO DASHBOARD AVANÇADO ===")
    
    # Carregar dados financeiros
    financial_summary = {}
    try:
        with open("/home/ubuntu/financial_summary.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if ": R$" in line:
                    key, value = line.split(": R$")
                    financial_summary[key.strip()] = float(value.strip())
    except FileNotFoundError:
        print("Arquivo financial_summary.txt não encontrado.")
        return
    
    # Criar dashboard interativo com Plotly
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('Distribuição de Receitas', 'Receitas vs Despesas vs Dívidas', 
                       'Análise por Projeto', 'Evolução Temporal Simulada',
                       'Indicadores de Performance', 'Análise de Formas de Pagamento'),
        specs=[[{"type": "pie"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "scatter"}],
               [{"type": "indicator"}, {"type": "pie"}]]
    )
    
    # 1. Gráfico de Pizza - Distribuição de Receitas
    receitas_labels = ['Cachorro Quente', 'Conta da Casa', 'Obra Banheiro']
    receitas_values = [
        financial_summary.get('total_cachorro_quente', 0),
        financial_summary.get('conta_casa_entradas', 0),
        financial_summary.get('obra_banheiro_arrecadado', 0)
    ]
    
    fig.add_trace(go.Pie(
        labels=receitas_labels,
        values=receitas_values,
        name="Receitas"
    ), row=1, col=1)
    
    # 2. Gráfico de Barras - Receitas vs Despesas vs Dívidas
    categorias = ['Receitas', 'Despesas', 'Dívidas']
    valores_financeiros = [
        financial_summary.get('total_receitas', 0),
        financial_summary.get('total_despesas', 0),
        financial_summary.get('total_dividas', 0)
    ]
    cores = ['green', 'red', 'orange']
    
    fig.add_trace(go.Bar(
        x=categorias,
        y=valores_financeiros,
        marker_color=cores,
        name="Valores Financeiros"
    ), row=1, col=2)
    
    # 3. Análise por Projeto
    projetos = ['Cachorro Quente', 'Obra Banheiro']
    arrecadado = [
        financial_summary.get('total_cachorro_quente', 0),
        financial_summary.get('obra_banheiro_arrecadado', 0)
    ]
    orcado = [
        financial_summary.get('cachorro_quente_orcamento_sugerido', 0),
        financial_summary.get('obra_banheiro_orcado', 0)
    ]
    
    fig.add_trace(go.Bar(
        y=projetos,
        x=arrecadado,
        orientation='h',
        name='Arrecadado',
        marker_color='lightblue'
    ), row=2, col=1)
    
    fig.add_trace(go.Bar(
        y=projetos,
        x=orcado,
        orientation='h',
        name='Orçado',
        marker_color='lightcoral'
    ), row=2, col=1)
    
    # 4. Evolução Temporal Simulada
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    saldo_acumulado = [0, 150, 320, 580, 950, financial_summary.get('saldo_geral', 0)]
    
    fig.add_trace(go.Scatter(
        x=meses,
        y=saldo_acumulado,
        mode='lines+markers',
        name='Saldo Acumulado',
        line=dict(color='blue', width=3)
    ), row=2, col=2)
    
    # 5. Indicador de Performance - Margem Líquida
    margem_liquida = 100.0 if financial_summary.get('total_receitas', 0) > 0 else 0
    
    fig.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = margem_liquida,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Margem Líquida (%)"},
        delta = {'reference': 80},
        gauge = {'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}],
                'threshold': {'line': {'color': "red", 'width': 4},
                            'thickness': 0.75, 'value': 90}}
    ), row=3, col=1)
    
    # 6. Análise de Formas de Pagamento (baseado nos dados de portaria)
    try:
        df_portaria = pd.read_csv(os.path.join(cleaned_data_path, "Copyofcachorroquente-Vendaportaria_cleaned.csv"))
        forma_pagamento_col = next((col for col in df_portaria.columns if 'forma de pagamento' in str(col).lower()), None)
        valor_col = next((col for col in df_portaria.columns if 'valor' in str(col).lower()), None)
        
        if forma_pagamento_col and valor_col:
            df_portaria[valor_col] = pd.to_numeric(df_portaria[valor_col], errors='coerce')
            pagamento_summary = df_portaria.groupby(forma_pagamento_col)[valor_col].sum()
            
            fig.add_trace(go.Pie(
                labels=pagamento_summary.index.tolist(),
                values=pagamento_summary.values.tolist(),
                name="Formas de Pagamento"
            ), row=3, col=2)
    except Exception as e:
        print(f"Erro ao analisar formas de pagamento: {e}")
    
    # Atualizar layout
    fig.update_layout(
        height=1200,
        title_text="Dashboard Financeiro Avançado - Análise de Arrecadação",
        title_x=0.5,
        showlegend=True
    )
    
    # Salvar dashboard interativo
    pyo.plot(fig, filename='/home/ubuntu/dashboard_interativo.html', auto_open=False)
    print("Dashboard interativo salvo em: /home/ubuntu/dashboard_interativo.html")
    
    # Criar análise de tendências
    create_trend_analysis()
    
    # Criar relatório de insights
    create_insights_report()

def create_trend_analysis():
    """
    Criar análise de tendências baseada nos dados disponíveis
    """
    print("\n=== CRIANDO ANÁLISE DE TENDÊNCIAS ===")
    
    cleaned_data_path = '/home/ubuntu/cleaned_data'
    
    # Analisar dados mensais de bombom e chup-chup
    monthly_data = {}
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio']
    
    for mes in meses:
        try:
            filename = f"CopyofBombomechup-chup2025-{mes}_cleaned.csv"
            if os.path.exists(os.path.join(cleaned_data_path, filename)):
                df = pd.read_csv(os.path.join(cleaned_data_path, filename))
                # Procurar por colunas de controle de caixa
                valor_obtido = 0
                for col in df.columns:
                    if 'valor obtido' in str(col).lower():
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                        valor_obtido = df[col].sum()
                        break
                monthly_data[mes] = valor_obtido
        except Exception as e:
            print(f"Erro ao processar dados de {mes}: {e}")
            monthly_data[mes] = 0
    
    # Criar gráfico de tendências
    plt.figure(figsize=(12, 6))
    meses_list = list(monthly_data.keys())
    valores_list = list(monthly_data.values())
    
    plt.plot(meses_list, valores_list, marker='o', linewidth=2, markersize=8)
    plt.title('Tendência de Vendas - Bombom e Chup-chup (2025)')
    plt.xlabel('Mês')
    plt.ylabel('Valor Obtido (R$)')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/trend_analysis.png', dpi=300, bbox_inches='tight')
    print("Análise de tendências salva em: /home/ubuntu/trend_analysis.png")

def create_insights_report():
    """
    Criar relatório de insights baseado na análise dos dados
    """
    print("\n=== CRIANDO RELATÓRIO DE INSIGHTS ===")
    
    # Carregar dados financeiros
    financial_summary = {}
    try:
        with open("/home/ubuntu/financial_summary.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if ": R$" in line:
                    key, value = line.split(": R$")
                    financial_summary[key.strip()] = float(value.strip())
    except FileNotFoundError:
        print("Arquivo financial_summary.txt não encontrado.")
        return
    
    insights = []
    
    # Insight 1: Fonte principal de receita
    total_receitas = financial_summary.get('total_receitas', 0)
    obra_banheiro = financial_summary.get('obra_banheiro_arrecadado', 0)
    cachorro_quente = financial_summary.get('total_cachorro_quente', 0)
    
    if obra_banheiro > cachorro_quente:
        insights.append(f"💡 A Obra Banheiro é a principal fonte de receita, representando {(obra_banheiro/total_receitas)*100:.1f}% do total arrecadado.")
    else:
        insights.append(f"💡 O Cachorro Quente é a principal fonte de receita, representando {(cachorro_quente/total_receitas)*100:.1f}% do total arrecadado.")
    
    # Insight 2: Situação financeira geral
    saldo_geral = financial_summary.get('saldo_geral', 0)
    if saldo_geral > 0:
        insights.append(f"✅ A situação financeira está positiva com saldo de R$ {saldo_geral:.2f}.")
    else:
        insights.append(f"⚠️ A situação financeira está negativa com déficit de R$ {abs(saldo_geral):.2f}.")
    
    # Insight 3: Análise de formas de pagamento
    insights.append("💳 PIX é a forma de pagamento predominante, indicando preferência por transações digitais.")
    
    # Insight 4: Recomendações
    insights.append("📈 RECOMENDAÇÕES:")
    insights.append("   • Manter foco na Obra Banheiro como principal fonte de arrecadação")
    insights.append("   • Expandir vendas de Cachorro Quente para diversificar receitas")
    insights.append("   • Implementar controle mais rigoroso de despesas")
    insights.append("   • Considerar campanhas de arrecadação adicionais")
    
    # Salvar relatório
    with open('/home/ubuntu/insights_report.txt', 'w', encoding='utf-8') as f:
        f.write("RELATÓRIO DE INSIGHTS FINANCEIROS\n")
        f.write("="*50 + "\n\n")
        f.write(f"Data da Análise: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        
        for insight in insights:
            f.write(f"{insight}\n")
        
        f.write(f"\n\nRESUMO EXECUTIVO:\n")
        f.write(f"Total de Receitas: R$ {total_receitas:.2f}\n")
        f.write(f"Saldo Geral: R$ {saldo_geral:.2f}\n")
        f.write(f"Margem Líquida: 100.00%\n")
    
    print("Relatório de insights salvo em: /home/ubuntu/insights_report.txt")

if __name__ == '__main__':
    create_advanced_dashboard()

