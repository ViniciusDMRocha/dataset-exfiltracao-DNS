import pandas as pd
import os

diretorio_base = os.path.dirname(os.path.abspath(__file__))
PASTA_ENTRADA = os.path.join(diretorio_base, "csv_benigno")

# Nome do arquivo que você deseja processar
NOME_ARQUIVO_ALVO = "Dia7_Do53_benigno.csv"

ARQUIVO_ENTRADA = os.path.join(PASTA_ENTRADA, NOME_ARQUIVO_ALVO)
ARQUIVO_SAIDA = os.path.join(PASTA_ENTRADA, "Amostra_Do53_Benigno.csv")

QTD_AMOSTRAS = 100000
FILTRAR_LABEL_ZERO = True

def criar_amostra():
    if not os.path.exists(ARQUIVO_ENTRADA):
        print(f"Arquivo não encontrado: {ARQUIVO_ENTRADA}")
        return

    print(f"Carregando arquivo: {ARQUIVO_ENTRADA}")
    
    df = pd.read_csv(ARQUIVO_ENTRADA)
    
    total_linhas = len(df)
    print(f"Total de linhas no arquivo: {total_linhas}")

    if FILTRAR_LABEL_ZERO and 'label' in df.columns:
        print("Filtrando apenas Label 0")
        df = df[df['label'] == 0]
    
    if len(df) < QTD_AMOSTRAS:
        df_amostra = df
    else:
       
        print(f"Selecionando {QTD_AMOSTRAS} linhas aleatórias")
        # random_state=42 garante que o trabalho possa ser reproduzido
        df_amostra = df.sample(n=QTD_AMOSTRAS, random_state=42)


    print(f"Salvando em: {ARQUIVO_SAIDA}")
    df_amostra.to_csv(ARQUIVO_SAIDA, index=False)
    
    print(f"Arquivo gerado com {len(df_amostra)} linhas.")

if __name__ == "__main__":
    criar_amostra()