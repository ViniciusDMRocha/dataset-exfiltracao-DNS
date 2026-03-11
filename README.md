
# Documentação da Extração de Dados com NFStream

## 1. Visão Geral
Este documento descreve o processo de extração de fluxos de tráfego de rede a partir de arquivos `.pcapng` utilizando a biblioteca **NFStream**. O objetivo foi transformar capturas de tráfego em conjuntos de dados tabulares para análise de tráfego benigno e potencialmente malicioso.

---

## 2. Ferramenta Utilizada
- **NFStream**: Framework para extração de features de tráfego de rede a partir de capturas (`pcap`, `pcapng`) ou interfaces em tempo real.
- Vantagens:
  - Extração padronizada de múltiplas features.
  - Suporte a classificação de aplicações e protocolos.
  - Integração direta com **pandas** para análise e exportação.

---

## 3. Fluxo de Extração

### 3.1 Script Base Utilizado
```python
import pandas as pd
from datetime import datetime
from nfstream import NFStreamer

streamer = NFStreamer(source="/mnt/c/Faculdade/TCC/pcap/Dia10_DoH_Benigno.pcapng")

df = pd.DataFrame([{
    "src_ip": flow.src_ip,
    "dst_ip": flow.dst_ip,
    "src_port": flow.src_port,
    "dst_port": flow.dst_port,
    "protocol": flow.protocol,
    "application_name": flow.application_name,
    "requested_server_name": flow.requested_server_name,
    "bidirectional_bytes": flow.bidirectional_bytes,
    "bidirectional_packets": flow.bidirectional_packets,
    "src2dst_bytes": flow.src2dst_bytes,
    "dst2src_bytes": flow.dst2src_bytes,
    "bidirectional_duration_ms": flow.bidirectional_duration_ms,
    "start_time": datetime.fromtimestamp(flow.bidirectional_first_seen_ms / 1000),
    "end_time": datetime.fromtimestamp(flow.bidirectional_last_seen_ms / 1000)
} for flow in streamer])

df.to_csv("/mnt/c/Faculdade/TCC/csv/Dia10_DoH_Benigno.csv", index=False)
```

### 3.2 Detalhes da Extração
- Fonte: Arquivos `.pcapng` capturados previamente.
- Saída: Arquivos `.csv` contendo os fluxos e atributos escolhidos.

---

## 4. Features Selecionadas
As seguintes features foram extraídas do objeto `flow` do NFStream:

- `src_ip`, `dst_ip`
- `src_port`, `dst_port`
- `protocol`
- `application_name`
- `requested_server_name`
- `bidirectional_bytes`
- `bidirectional_packets`
- `src2dst_bytes`
- `dst2src_bytes`
- `bidirectional_duration_ms`
- `start_time` (calculado a partir de `bidirectional_first_seen_ms`)
- `end_time` (calculado a partir de `bidirectional_last_seen_ms`)

Essas features permitem analisar tráfego DNS/DoH em nível de fluxo, verificando intensidade, duração e características da comunicação.

---

## 5. Rotulagem
- Inicialmente, a rotulagem foi feita a partir do **contexto da captura** (ex.: `DiaX_DoH_Benigno` → tráfego benigno).
- Posteriormente, foi aplicado filtro por **porta/protocolo**:
  - Ex.: Se `dst_port == 53` (DNS) ou `dst_port == 443` (DoH), rotulado como *benigno*.
  - Caso contrário, rotulado como *outlier*.

---

## 6. Filtragem dos Dados
Após a geração dos CSVs:
- Foram removidos fluxos não relacionados a DNS/DoH.
- Foi aplicado filtro pela coluna `label` para separar tráfego **benigno** de **outliers**.

---

## 7. Considerações Finais
- O NFStream gera fluxos agregados, portanto pode haver divergência no número de fluxos em comparação com outras ferramentas (ex.: **Argus**).
- Essa diferença é esperada devido às estratégias internas de agregação e expiração de fluxos.
- Para consistência, todo o pipeline foi padronizado com NFStream.
