# Camada de lógica e manipulação de dados
# Funções de carregamento e limpeza dos dados

import pandas as pd
from datetime import date

def carregar_dados(caminho_excel: str = "data/Chamados Geral - API Periodo.xlsx") -> pd.DataFrame:
    """Carrega o Excel e trata os dados iniciais"""
    df = pd.read_excel(caminho_excel)
    df.columns = [col.strip() for col in df.columns]  # remove espaços
    return df


def preparar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Converte datas e adiciona colunas úteis"""
    if "Data de Abertura" in df.columns:
        df["Data de Abertura"] = pd.to_datetime(df["Data de Abertura"], errors="coerce")
    if "Data Limite" in df.columns:
        df["Data Limite"] = pd.to_datetime(df["Data Limite"], errors="coerce")

    # Calcula SLA (dias restantes)
    if "Data Limite" in df.columns:
        df["Dias Restantes"] = (df["Data Limite"] - pd.Timestamp(date.today())).dt.days

    # Classifica chamados vencidos
    df["Status SLA"] = df["Dias Restantes"].apply(
        lambda x: "Vencido" if pd.notna(x) and x < 0 else "No prazo"
    )

    return df
