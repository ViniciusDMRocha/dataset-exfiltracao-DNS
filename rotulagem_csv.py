import pandas as pd
import os
import glob
import gc

BASE_PATH = "/mnt/c/Faculdade/TCC"
PATH_BENIGNO = os.path.join(BASE_PATH, "csv_benigno_amostra")
PATH_MALIGNO = os.path.join(BASE_PATH, "csv_exfiltracao")


PATH_TEMP = os.path.join(BASE_PATH, "arquivos_rotulados")
os.makedirs(PATH_TEMP, exist_ok=True)

ARQUIVO_FINAL = os.path.join(BASE_PATH, "dataset_final.csv")

def limpar_e_salvar_separado(caminho_arquivo, label):
    nome_original = os.path.basename(caminho_arquivo)
    nome_limpo = f"rotulado_{nome_original}"
    caminho_saida = os.path.join(PATH_TEMP, nome_limpo)
    
    if os.path.exists(caminho_saida):
        print(f"Já processado: {nome_limpo}")
        return caminho_saida

    try:
        print(f"Processando: {nome_original} ... ", end="")
        
        df = pd.read_csv(caminho_arquivo)
        df['label'] = label
        
        filtro_portas = (df['src_port'].isin([53, 443])) | (df['dst_port'].isin([53, 443]))
        df = df[filtro_portas]
        
        filtro_proto = df['protocol'].isin([6, 17])
        df = df[filtro_proto]
        
        df = df[df['bidirectional_packets'] > 0]
        df = df.fillna(0)
        
        if len(df) > 0:
            df.to_csv(caminho_saida, index=False)
            print(f"Salvo ({len(df)} linhas)")
            resultado = caminho_saida
        else:
            print(f"Vazio após filtros")
            resultado = None

        del df
        gc.collect()
        return resultado

    except Exception as e:
        print(f"Erro crítico em {nome_original}: {e}")
        return None


print("Aplicando filtros")

arquivos_prontos = []

print("\n Lendo Benignos...")
lista_benignos = glob.glob(os.path.join(PATH_BENIGNO, "*.csv"))
for arq in lista_benignos:
    res = limpar_e_salvar_separado(arq, 0)
    if res: arquivos_prontos.append(res)

print("\n Lendo Exfiltração...")
lista_malignos = glob.glob(os.path.join(PATH_MALIGNO, "*.csv"))
for arq in lista_malignos:
    res = limpar_e_salvar_separado(arq, 1)
    if res: arquivos_prontos.append(res)


if len(arquivos_prontos) == 0:
    print("Nenhum arquivo sobrou após os filtros!")
    exit()

if os.path.exists(ARQUIVO_FINAL):
    os.remove(ARQUIVO_FINAL)

with open(arquivos_prontos[0], 'r') as f:
    cabecalho = f.readline()

with open(ARQUIVO_FINAL, 'w') as outfile:
    outfile.write(cabecalho)
    
    for i, arq in enumerate(arquivos_prontos):
        nome = os.path.basename(arq)
        
        with open(arq, 'r') as infile:
            next(infile)
            
            for line in infile:
                outfile.write(line)

print(f"{ARQUIVO_FINAL}")
