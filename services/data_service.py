import pandas as pd
from datetime import date
import os

def carregar_dados(caminho_excel: str = None) -> pd.DataFrame:
    """Carrega o Excel e trata os dados iniciais, com detecção automática de cabeçalho"""
    if caminho_excel is None:
        caminho_excel = os.path.join(os.path.dirname(__file__), "..", "data", "Chamdos Geral - API Periodo.xlsx")
        caminho_excel = os.path.abspath(caminho_excel)

    if not os.path.exists(caminho_excel):
        st.error(f"❌ Arquivo Excel não encontrado em:\n{caminho_excel}")
        st.stop()

    try:
        # tenta ler com cabeçalho automático
        df = pd.read_excel(caminho_excel)
        if df.shape[1] <= 1 or df.dropna(how="all").shape[0] == 0:
            # se vier vazio, tenta pular linhas iniciais
            for i in range(1, 10):
                df = pd.read_excel(caminho_excel, skiprows=i)
                if df.dropna(how="all").shape[0] > 0 and df.shape[1] > 1:
                    break

        # limpa nomes de colunas
        df.columns = [str(col).replace("Column1.", "").strip() for col in df.columns]
        df = df.dropna(how="all")
        return df

    except Exception as e:
        st.error(f"❌ Erro ao ler o arquivo Excel:\n{e}")
        st.stop()


def preparar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Converte datas e adiciona colunas úteis"""
    if "start" in df.columns:
        df["Data de Abertura"] = pd.to_datetime(df["start"], errors="coerce")

    # Define Data Limite = 10 dias após abertura
    df["Data Limite"] = df["Data de Abertura"] + pd.to_timedelta(10, unit="D")

    # Calcula dias restantes até o vencimento
    df["Dias Restantes"] = (df["Data Limite"] - pd.Timestamp(date.today())).dt.days

    # Classifica chamados vencidos ou dentro do prazo
    df["Status SLA"] = df["Dias Restantes"].apply(
        lambda x: "Vencido" if pd.notna(x) and x < 0 else "No prazo"
    )

    return df
