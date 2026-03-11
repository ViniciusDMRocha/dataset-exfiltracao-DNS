import pandas as pd
from datetime import datetime
from nfstream import NFStreamer
import os
import math
from collections import Counter

# --- CONFIGURAÇÕES ---

# Benigno
pasta_pcap = "/mnt/c/Faculdade/TCC/pcap_benigno"
pasta_csv = "/mnt/c/Faculdade/TCC/csv_benigno"

# Exfiltração
# pasta_pcap = "/mnt/c/Faculdade/TCC/pcap_exfiltracao"
# pasta_csv = "/mnt/c/Faculdade/TCC/csv_exfiltracao"

os.makedirs(pasta_csv, exist_ok=True)

# LISTA DE ATRIBUTOS
FEATURES_FIXAS = [
    # Identificadores (remover antes do treino, mas uteis agora)
    "src_ip", "dst_ip", "src_port", "dst_port", "protocol", 
    "start_time", "end_time", 
    
    # Estatísticas Brutas
    "bidirectional_bytes", "bidirectional_packets", "bidirectional_duration_ms",
    "src2dst_bytes", "dst2src_bytes",
    
    # Camada de Aplicação / DNS
    "application_name", "application_category_name", "requested_server_name",
    
    # Features Criadas
    "dns_query_length", "dns_query_entropy", "dns_subdomain_count", "dns_numerical_ratio"
]

def calcular_entropia(texto):
    if not texto: return 0.0
    contador = Counter(texto)
    tamanho = len(texto)
    probabilidades = [count / tamanho for count in contador.values()]
    return -sum(p * math.log2(p) for p in probabilidades)

def extrair_dados_padronizados(flow):
    # 1. Cria um dicionário base com TUDO zerado ou vazio
    dados = {k: None for k in FEATURES_FIXAS}
    
    # 2. Preenche com o que o nfstream encontrou
    for atributo in dir(flow):
        if atributo in dados: # Só pega se estiver na nossa Lista Mestra
            val = getattr(flow, atributo)
            # Tratamento de datas
            if atributo == "bidirectional_first_seen_ms": # mapear se necessário
                 pass 
            else:
                dados[atributo] = val

    # Ajuste manual de datas (se os nomes diferem da lista mestra)
    dados["start_time"] = datetime.fromtimestamp(flow.bidirectional_first_seen_ms / 1000)
    dados["end_time"] = datetime.fromtimestamp(flow.bidirectional_last_seen_ms / 1000)

    # 3. Engenharia de Features (Sempre roda)
    domain = getattr(flow, "requested_server_name", "")
    if domain is None: domain = ""
    
    dados["dns_query_length"] = len(domain)
    dados["dns_query_entropy"] = calcular_entropia(domain)
    dados["dns_subdomain_count"] = domain.count(".") + 1 if domain else 0
    numeros = sum(c.isdigit() for c in domain)
    dados["dns_numerical_ratio"] = numeros / len(domain) if domain else 0.0
    
    return dados

chunk_size = 50000 

print("⚠️  ATENÇÃO: Apagando CSVs antigos para evitar inconsistência...")
for f in os.listdir(pasta_csv):
    if f.endswith(".csv"):
        os.remove(os.path.join(pasta_csv, f))

for nome_arquivo in os.listdir(pasta_pcap):
    if nome_arquivo.endswith(".pcapng") or nome_arquivo.endswith(".pcap"): # Aceita .pcap tb
        caminho_pcap = os.path.join(pasta_pcap, nome_arquivo)
        tamanho_arq = os.path.getsize(caminho_pcap)
        
        if tamanho_arq == 0: continue
            
        print(f"Processando: {nome_arquivo}...")

        streamer = NFStreamer(source=caminho_pcap)
        nome_csv = nome_arquivo.replace(".pcapng", ".csv").replace(".pcap", ".csv")
        caminho_csv = os.path.join(pasta_csv, nome_csv)

        buffer = []
        primeira_escrita = True
        
        for i, flow in enumerate(streamer, start=1):
            # Usamos a nova função padronizada
            buffer.append(extrair_dados_padronizados(flow))

            if i % chunk_size == 0:
                df = pd.DataFrame(buffer)
                # Garante a ordem das colunas
                df = df[FEATURES_FIXAS] 
                # Salva
                df.to_csv(caminho_csv, mode="a", header=primeira_escrita, index=False)
                primeira_escrita = False
                buffer = []

        if buffer:
            df = pd.DataFrame(buffer)
            df = df[FEATURES_FIXAS]
            df.to_csv(caminho_csv, mode="a", header=primeira_escrita, index=False)
        
        print(f"-> Salvo: {caminho_csv}")

print("\n--- Processamento concluído ---")