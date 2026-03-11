import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# 1. Configuração de Pastas
OUTPUT_DIR = 'imagens_aed'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Carregar o dataset
try:
    df = pd.read_csv('dataset_final.csv')
    print(f"Dataset carregado! Total de registros: {len(df)}")
except FileNotFoundError:
    print("Erro: Arquivo 'dataset_tcc_final.csv' não encontrado.")
    exit()

# --- MATRIZ DE CORRELAÇÃO DE PEARSON ---

numeric_df = df.select_dtypes(include=[np.number])
corr_matrix_full_data = numeric_df.corr() 
corr_matrix_abs = corr_matrix_full_data.abs()

upper = corr_matrix_abs.where(np.triu(np.ones(corr_matrix_abs.shape), k=1).astype(bool))
to_drop = [column for column in upper.columns if any(upper[column] > 0.90) and column != 'label']

# 1. GERAR MATRIZ FILTRADA
plt.figure(figsize=(16, 12))
df_filtrado = numeric_df.drop(columns=to_drop)
corr_matrix_filtered = df_filtrado.corr()

sns.heatmap(corr_matrix_filtered, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, annot_kws={"size": 10})
plt.title('Matriz de Correlação de Pearson - Sem Redundâncias (>0.90)', fontsize=15)
plt.tight_layout()

path_filtrada = os.path.join(OUTPUT_DIR, 'matriz_correlacao_filtrada.png')
plt.savefig(path_filtrada, bbox_inches='tight', dpi=300)
plt.close()

# 2. GERAR MATRIZ COMPLETA
plt.figure(figsize=(18, 14))
sns.heatmap(corr_matrix_full_data, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, annot_kws={"size": 8})
plt.title('Matriz de Correlação de Pearson - Completa', fontsize=15)
plt.tight_layout()

path_completa = os.path.join(OUTPUT_DIR, 'matriz_correlacao.png')
plt.savefig(path_completa, bbox_inches='tight', dpi=300)
plt.close()

print(f"Colunas removidas por alta correlação: {to_drop}")

# --- MÉTODO DE TUKEY ---

# Lista completa de atributos conforme solicitado
features_analise = [
    'dns_query_entropy', 
    'dns_query_length', 
    'dns_numerical_ratio', 
    'dns_subdomain_count',
    'bidirectional_packets', 
    'bidirectional_duration_ms', 
    'src2dst_bytes'
]

print("\nGerando Boxplots individuais...")

for feature in features_analise:
    if feature in df.columns:
        plt.figure(figsize=(10, 6))
        
        sns.boxplot(x='label', y=feature, data=df, hue='label', palette='Set2', legend=False)
        
        plt.title(f'Distribuição de {feature} por Classe', fontsize=14)
        plt.xlabel('Classe (0: Benigno, 1: Exfiltração)', fontsize=12)
        plt.ylabel('Valor Obtido', fontsize=12)
        
        file_name = f'boxplot_{feature}.png'
        path_save = os.path.join(OUTPUT_DIR, file_name)
        plt.savefig(path_save, bbox_inches='tight')
        plt.close()
        
        print(f"{file_name} salvo.")
    else:
        print(f"Aviso: Atributo '{feature}' não encontrado no CSV.")

print(f"\nProcesso concluído")