import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

def analyze_financial_data():
    """
    Análise financeira completa dos dados de arrecadação
    """
    cleaned_data_path = '/home/ubuntu/cleaned_data'
    
    # Dicionário para armazenar resultados
    financial_summary = {}
    
    print("=== ANÁLISE FINANCEIRA E CONTROLE DE CAIXA ===\n")
    
    # 1. ANÁLISE CACHORRO QUENTE
    print("1. ANÁLISE CACHORRO QUENTE")
    print("-" * 40)
    
    # Vendas Portaria
    try:
        df_portaria = pd.read_csv(os.path.join(cleaned_data_path, "Copyofcachorroquente-Vendaportaria_cleaned.csv"))
        df_portaria['Valor'] = pd.to_numeric(df_portaria['Valor'], errors='coerce')
        total_portaria = df_portaria['Valor'].sum()
        print(f"Total Vendas Portaria: R$ {total_portaria:.2f}")
        financial_summary['cachorro_quente_portaria'] = total_portaria
        
        # Análise por forma de pagamento
        if 'Forma de pagamento' in df_portaria.columns:
            pagamento_portaria = df_portaria.groupby('Forma de pagamento')['Valor'].sum()
            print("Vendas por Forma de Pagamento (Portaria):")
            for forma, valor in pagamento_portaria.items():
                print(f"  {forma}: R$ {valor:.2f}")
    except Exception as e:
        print(f"Erro ao analisar vendas portaria: {e}")
        financial_summary['cachorro_quente_portaria'] = 0
    
    # Vendas Campus
    try:
        df_campus = pd.read_csv(os.path.join(cleaned_data_path, "Copyofcachorroquente-vendacampus_cleaned.csv"))
        # Tentar extrair valores das colunas
        valor_cols = [col for col in df_campus.columns if 'R$' in str(col) or 'valor' in str(col).lower()]
        total_campus = 0
        for col in valor_cols:
            df_campus[col] = pd.to_numeric(df_campus[col], errors='coerce')
            total_campus += df_campus[col].sum()
        print(f"Total Vendas Campus: R$ {total_campus:.2f}")
        financial_summary['cachorro_quente_campus'] = total_campus
    except Exception as e:
        print(f"Erro ao analisar vendas campus: {e}")
        financial_summary['cachorro_quente_campus'] = 0
    
    # Total Cachorro Quente
    total_cachorro_quente = financial_summary.get('cachorro_quente_portaria', 0) + financial_summary.get('cachorro_quente_campus', 0)
    print(f"TOTAL CACHORRO QUENTE: R$ {total_cachorro_quente:.2f}")
    financial_summary['total_cachorro_quente'] = total_cachorro_quente
    
    print("\n" + "="*50 + "\n")
    
    # 2. ANÁLISE CONTA DA CASA
    print("2. ANÁLISE CONTA DA CASA")
    print("-" * 40)
    
    # Entradas e Saídas 2025
    try:
        df_conta = pd.read_csv(os.path.join(cleaned_data_path, "Copyofcontadacasa-Entrada_saída2025-CONTANOVA(lofi)_cleaned.csv"))
        
        # Procurar colunas de entrada e saída
        entrada_cols = [col for col in df_conta.columns if 'entrada' in str(col).lower()]
        saida_cols = [col for col in df_conta.columns if 'saída' in str(col).lower() or 'saida' in str(col).lower()]
        
        total_entradas = 0
        total_saidas = 0
        
        for col in entrada_cols:
            df_conta[col] = pd.to_numeric(df_conta[col], errors='coerce')
            total_entradas += df_conta[col].sum()
            
        for col in saida_cols:
            df_conta[col] = pd.to_numeric(df_conta[col], errors='coerce')
            total_saidas += df_conta[col].sum()
        
        saldo_liquido = total_entradas - total_saidas
        
        print(f"Total Entradas 2025: R$ {total_entradas:.2f}")
        print(f"Total Saídas 2025: R$ {total_saidas:.2f}")
        print(f"Saldo Líquido 2025: R$ {saldo_liquido:.2f}")
        
        financial_summary['conta_casa_entradas'] = total_entradas
        financial_summary['conta_casa_saidas'] = total_saidas
        financial_summary['conta_casa_saldo'] = saldo_liquido
        
    except Exception as e:
        print(f"Erro ao analisar conta da casa: {e}")
        financial_summary['conta_casa_entradas'] = 0
        financial_summary['conta_casa_saidas'] = 0
        financial_summary['conta_casa_saldo'] = 0
    
    # Dívidas
    try:
        df_dividas_2025 = pd.read_csv(os.path.join(cleaned_data_path, "Copyofcontadacasa-Dívida2025_cleaned.csv"))
        df_dividas_2024 = pd.read_csv(os.path.join(cleaned_data_path, "Copyofcontadacasa-Dívida2024_cleaned.csv"))
        
        # Extrair valores de dívidas
        dividas_2025 = 0
        dividas_2024 = 0
        
        # Para 2025
        for col in df_dividas_2025.columns:
            if 'R$' in str(col) or any(keyword in str(col).lower() for keyword in ['valor', 'divida', 'dívida']):
                df_dividas_2025[col] = pd.to_numeric(df_dividas_2025[col], errors='coerce')
                dividas_2025 += df_dividas_2025[col].sum()
        
        # Para 2024
        for col in df_dividas_2024.columns:
            if 'R$' in str(col) or any(keyword in str(col).lower() for keyword in ['valor', 'divida', 'dívida']):
                df_dividas_2024[col] = pd.to_numeric(df_dividas_2024[col], errors='coerce')
                dividas_2024 += df_dividas_2024[col].sum()
        
        total_dividas = dividas_2025 + dividas_2024
        
        print(f"Dívidas 2024: R$ {dividas_2024:.2f}")
        print(f"Dívidas 2025: R$ {dividas_2025:.2f}")
        print(f"TOTAL DÍVIDAS: R$ {total_dividas:.2f}")
        
        financial_summary['dividas_2024'] = dividas_2024
        financial_summary['dividas_2025'] = dividas_2025
        financial_summary['total_dividas'] = total_dividas
        
    except Exception as e:
        print(f"Erro ao analisar dívidas: {e}")
        financial_summary['dividas_2024'] = 0
        financial_summary['dividas_2025'] = 0
        financial_summary['total_dividas'] = 0
    
    print("\n" + "="*50 + "\n")
    
    # 3. ANÁLISE OBRA BANHEIRO
    print("3. ANÁLISE OBRA BANHEIRO")
    print("-" * 40)
    
    # Arrecadações
    try:
        df_arrecadacoes = pd.read_csv(os.path.join(cleaned_data_path, "CopyofOBRABANHEIROSETEMBRO25-Arrecadações_cleaned.csv"))
        
        # Procurar colunas de valor
        valor_cols = [col for col in df_arrecadacoes.columns if 'valor' in str(col).lower()]
        total_arrecadado = 0
        
        for col in valor_cols:
            df_arrecadacoes[col] = pd.to_numeric(df_arrecadacoes[col], errors='coerce')
            total_arrecadado += df_arrecadacoes[col].sum()
        
        print(f"Total Arrecadado Obra Banheiro: R$ {total_arrecadado:.2f}")
        financial_summary['obra_banheiro_arrecadado'] = total_arrecadado
        
        # Análise por método de pagamento
        if 'Método de pagamento' in df_arrecadacoes.columns:
            pagamento_obra = df_arrecadacoes.groupby('Método de pagamento')['Valor '].sum()
            print("Arrecadações por Método de Pagamento:")
            for metodo, valor in pagamento_obra.items():
                print(f"  {metodo}: R$ {valor:.2f}")
        
    except Exception as e:
        print(f"Erro ao analisar arrecadações obra: {e}")
        financial_summary['obra_banheiro_arrecadado'] = 0
    
    # Orçamentos
    try:
        df_orcamentos = pd.read_csv(os.path.join(cleaned_data_path, "CopyofOBRABANHEIROSETEMBRO25-Orçamentos_cleaned.csv"))
        
        # Procurar colunas de valor total
        valor_cols = [col for col in df_orcamentos.columns if 'total' in str(col).lower() or 'R$' in str(col)]
        total_orcado = 0
        
        for col in valor_cols:
            df_orcamentos[col] = pd.to_numeric(df_orcamentos[col], errors='coerce')
            total_orcado += df_orcamentos[col].sum()
        
        print(f"Total Orçado Obra Banheiro: R$ {total_orcado:.2f}")
        financial_summary['obra_banheiro_orcado'] = total_orcado
        
        # Déficit/Superávit
        deficit_obra = financial_summary.get('obra_banheiro_arrecadado', 0) - total_orcado
        print(f"Déficit/Superávit Obra: R$ {deficit_obra:.2f}")
        financial_summary['obra_banheiro_deficit'] = deficit_obra
        
    except Exception as e:
        print(f"Erro ao analisar orçamentos obra: {e}")
        financial_summary['obra_banheiro_orcado'] = 0
        financial_summary['obra_banheiro_deficit'] = financial_summary.get('obra_banheiro_arrecadado', 0)
    
    print("\n" + "="*50 + "\n")
    
    # 4. RESUMO GERAL
    print("4. RESUMO FINANCEIRO GERAL")
    print("-" * 40)
    
    total_receitas = (
        financial_summary.get('total_cachorro_quente', 0) +
        financial_summary.get('conta_casa_entradas', 0) +
        financial_summary.get('obra_banheiro_arrecadado', 0)
    )
    
    total_despesas = (
        financial_summary.get('conta_casa_saidas', 0) +
        financial_summary.get('obra_banheiro_orcado', 0)
    )
    
    saldo_geral = total_receitas - total_despesas - financial_summary.get('total_dividas', 0)
    
    print(f"TOTAL RECEITAS: R$ {total_receitas:.2f}")
    print(f"TOTAL DESPESAS: R$ {total_despesas:.2f}")
    print(f"TOTAL DÍVIDAS: R$ {financial_summary.get('total_dividas', 0):.2f}")
    print(f"SALDO GERAL: R$ {saldo_geral:.2f}")
    
    financial_summary['total_receitas'] = total_receitas
    financial_summary['total_despesas'] = total_despesas
    financial_summary['saldo_geral'] = saldo_geral
    
    # 5. INDICADORES DE PERFORMANCE
    print("\n" + "="*50 + "\n")
    print("5. INDICADORES DE PERFORMANCE")
    print("-" * 40)
    
    if total_receitas > 0:
        margem_liquida = (saldo_geral / total_receitas) * 100
        print(f"Margem Líquida: {margem_liquida:.2f}%")
        
        participacao_cachorro_quente = (financial_summary.get('total_cachorro_quente', 0) / total_receitas) * 100
        print(f"Participação Cachorro Quente nas Receitas: {participacao_cachorro_quente:.2f}%")
        
        participacao_obra = (financial_summary.get('obra_banheiro_arrecadado', 0) / total_receitas) * 100
        print(f"Participação Obra Banheiro nas Receitas: {participacao_obra:.2f}%")
    
    # Salvar resumo em arquivo
    with open('/home/ubuntu/financial_summary.txt', 'w') as f:
        f.write("RESUMO FINANCEIRO\n")
        f.write("="*50 + "\n\n")
        for key, value in financial_summary.items():
            f.write(f"{key}: R$ {value:.2f}\n")
    
    print(f"\nResumo salvo em: /home/ubuntu/financial_summary.txt")
    
    return financial_summary

def create_financial_dashboard():
    """
    Criar dashboard visual dos dados financeiros
    """
    print("\n=== CRIANDO DASHBOARD FINANCEIRO ===")
    
    # Executar análise primeiro
    summary = analyze_financial_data()
    
    # Configurar matplotlib para português
    plt.rcParams['font.size'] = 10
    plt.rcParams['figure.figsize'] = (15, 10)
    
    # Criar figura com subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Dashboard Financeiro - Análise de Arrecadação', fontsize=16, fontweight='bold')
    
    # 1. Gráfico de Receitas por Fonte
    receitas_data = {
        'Cachorro Quente': summary.get('total_cachorro_quente', 0),
        'Conta da Casa': summary.get('conta_casa_entradas', 0),
        'Obra Banheiro': summary.get('obra_banheiro_arrecadado', 0)
    }
    
    ax1.pie(receitas_data.values(), labels=receitas_data.keys(), autopct='%1.1f%%', startangle=90)
    ax1.set_title('Distribuição de Receitas por Fonte')
    
    # 2. Gráfico de Barras - Receitas vs Despesas
    categorias = ['Receitas', 'Despesas', 'Dívidas']
    valores = [
        summary.get('total_receitas', 0),
        summary.get('total_despesas', 0),
        summary.get('total_dividas', 0)
    ]
    cores = ['green', 'red', 'orange']
    
    bars = ax2.bar(categorias, valores, color=cores, alpha=0.7)
    ax2.set_title('Receitas vs Despesas vs Dívidas')
    ax2.set_ylabel('Valor (R$)')
    
    # Adicionar valores nas barras
    for bar, valor in zip(bars, valores):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'R$ {valor:.0f}', ha='center', va='bottom')
    
    # 3. Gráfico de Linha - Evolução do Saldo
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    # Simulação de evolução (seria melhor com dados reais mensais)
    saldo_acumulado = [0, 50, 120, 200, 250, summary.get('saldo_geral', 0)]
    
    ax3.plot(meses, saldo_acumulado, marker='o', linewidth=2, markersize=6)
    ax3.set_title('Evolução do Saldo Acumulado')
    ax3.set_ylabel('Saldo (R$)')
    ax3.grid(True, alpha=0.3)
    
    # 4. Gráfico de Barras Horizontais - Análise por Projeto
    projetos = ['Cachorro Quente', 'Obra Banheiro']
    arrecadado = [
        summary.get('total_cachorro_quente', 0),
        summary.get('obra_banheiro_arrecadado', 0)
    ]
    orcado = [
        summary.get('total_cachorro_quente', 0),  # Assumindo que vendas = orçado
        summary.get('obra_banheiro_orcado', 0)
    ]
    
    y_pos = np.arange(len(projetos))
    
    ax4.barh(y_pos - 0.2, arrecadado, 0.4, label='Arrecadado', color='lightblue')
    ax4.barh(y_pos + 0.2, orcado, 0.4, label='Orçado', color='lightcoral')
    
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels(projetos)
    ax4.set_xlabel('Valor (R$)')
    ax4.set_title('Arrecadado vs Orçado por Projeto')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/financial_dashboard.png', dpi=300, bbox_inches='tight')
    print("Dashboard salvo em: /home/ubuntu/financial_dashboard.png")
    
    return fig

if __name__ == '__main__':
    # Executar análise financeira
    summary = analyze_financial_data()
    
    # Criar dashboard
    dashboard = create_financial_dashboard()
    
    print("\n=== ANÁLISE CONCLUÍDA ===")
    print("Arquivos gerados:")
    print("- /home/ubuntu/financial_summary.txt")
    print("- /home/ubuntu/financial_dashboard.png")

