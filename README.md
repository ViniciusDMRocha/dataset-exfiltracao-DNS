# UFU-Exfiltração-DNS: Detecção de Exfiltração de Dados

Este repositório contém o ecossistema de desenvolvimento utilizado para a construção e estruturação de um conjunto de dados focado na identificação de exfiltração de dados via protocolo DNS (Do53). O projeto utiliza o framework **NFStream** para a extração de fluxos e técnicas de **Engenharia de Atributos** para a detecção de anomalias.

## Estrutura do Repositório

* **`pcap_benigno/`**: Diretório contendo as capturas brutas de tráfego legítimo.
* **`pcap_exfiltracao/`**: Diretório contendo as capturas brutas de cenários de ataque.
* **`imagens_aed/`**: Gráficos e visualizações gerados durante a Análise Exploratória de Dados.
* **`dataset_final.csv`**: Conjunto de dados consolidado e pronto para uso em modelos de ML.
* **Scripts Python (`.py`)**: Roteiros de automação para o pipeline de dados (raiz do projeto).

## Ambiente de Desenvolvimento e Instalação

O projeto foi executado em ambiente **WSL2 (Windows Subsystem for Linux)**. Para reproduzir o ambiente e instalar todas as dependências necessárias, execute o seguinte comando:

```bash
pip install nfstream pandas matplotlib seaborn scikit-learn
```

Requisitos Técnicos:

* **SO:** Windows 11 + Ubuntu 22.04 LTS (WSL2)
* **Linguagem:** Python 3.10.12
* **Principais Bibliotecas:**
    * `nfstream`: Extração de fluxos bidirecionais e Inspeção Profunda de Pacotes (DPI).
    * `pandas`: Manipulação de dados, filtragem e rotulagem.
    * `matplotlib` / `seaborn`: Geração de gráficos para análise exploratória.

## Como Reproduzir

Os arquivos PCAPNG originais necessários para alimentar as pastas pcap_benigno/ e pcap_exfiltracao/ estão disponíveis no link abaixo:

Google Drive: [Pasta de Dados Brutos](https://drive.google.com/drive/folders/1mhF6CBvu1TFPZRc24OVpSHZ3849n8I9I?usp=drive_link)

Nota: Os scripts dependem que os arquivos sejam baixados e mantidos com os nomes originais disponibilizados no link acima.

O funcionamento do código segue uma ordem lógica de transformação dos dados:

1. **Extração (`extrair_pcapng.py`)**: Converte arquivos PCAPNG em fluxos estruturados via NFStream, calculando métricas de entropia, comprimento de query e densidade numérica.
2. **Subamostragem (`gerador_amostra_benigna.py`)**: Realiza o *undersampling* de um dos arquivos CSV de tráfego benigno (previamente extraídos). O usuário deve selecionar um dos arquivos da base bruta para processamento, do qual o script extrairá uma amostra aleatória de 100.000 registros para consolidar o dataset final com realismo estatístico.
3. **Rotulagem e Limpeza (`rotulagem_csv.py`)**: Atribui rótulos binários (0 para Benigno, 1 para Exfiltração) e trata valores ausentes ou ruidosos. O script cria automaticamente uma pasta chamada `arquivos_rotulados` para salvar cada arquivo processado individualmente antes de consolidar o `dataset_final.csv`.
4. **Análise Exploratória (`analise_exploratoria.py`)**: Realiza a leitura do `dataset_final.csv`, gera métricas estatísticas e salva as visualizações na pasta `imagens_aed/`.

## Disponibilidade do Dataset Final

O principal produto deste trabalho — o conjunto de dados consolidado — está **publicamente disponível e hospedado no Mendeley Data**. Esta disponibilização visa facilitar a reprodutibilidade científica e oferecer uma base robusta para o treinamento de novos modelos de detecção de exfiltração via DNS.

* **Acesse aqui:** [Mendeley Data - UFU-Exfiltração-DNS](https://doi.org/10.17632/v2cy9y58t7.3)
* **DOI Oficial:** `10.17632/v2cy9y58t7.3`
* **Volume:** ~110.000 instâncias prontas para uso.
* **Proporção de Classes:** 10:1 (Benigno vs. Exfiltração), ideal para testes de resiliência a desbalanceamento.

Ao utilizar este dataset em pesquisas acadêmicas, solicita-se a citação via DOI conforme as diretrizes da plataforma.

---
*Este projeto foi desenvolvido como parte do Trabalho de Conclusão de Curso na Faculdade de Computação (FACOM) - UFU.*