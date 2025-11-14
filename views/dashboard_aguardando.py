# views/dashboard_aguardando.py
import streamlit as st
import plotly.express as px
import pandas as pd
import re

def mostrar_dashboard_aguardando(df):
    st.title("Dashboard Aguardando Aceite")

    # =========================================================
    # 1. KPI
    # =========================================================
    col1 = st.columns(3)[1]
    col1.metric("Chamados Totais (Abertos)", len(df))

    # =========================================================
    # 2. Botão de Atualização
    # =========================================================
    if st.button("Atualizar Dados do Google Sheets", key="refresh_google"):
        st.cache_data.clear()
        st.success("Dados atualizados manualmente!")
        st.rerun()

    # =========================================================
    # 3. EXTRAIR NÚMERO DA COLUNA "GERAL"
    # =========================================================
    def extrair_numero(texto):
        if pd.isna(texto):
            return None
        match = re.search(r'\((\d+)', str(texto))
        return int(match.group(1)) if match else None

    df["Geral_Numerico"] = df["Dias Restantes Geral"].apply(extrair_numero)

    # =========================================================
    # 4. FILTRO POR TÉCNICO (SIDEBAR)
    # =========================================================
    st.sidebar.header("Filtros")

    # Lista de técnicos únicos
    tecnicos_unicos = sorted([t for t in df["Técnico"].dropna().unique() if str(t).strip()])
    tecnico_filtro = st.sidebar.selectbox(
        "Filtrar por Técnico",
        options=["Todos"] + tecnicos_unicos,
        index=0,
        key="filtro_tecnico_sidebar"
    )

    # Aplica filtro
    if tecnico_filtro != "Todos":
        df_filtrado = df[df["Técnico"] == tecnico_filtro].copy()
    else:
        df_filtrado = df.copy()

    # =========================================================
    # 5. GRÁFICO (com filtro)
    # =========================================================
    st.subheader("Distribuição por Técnico")
    contagem = df_filtrado["Técnico"].value_counts().reset_index()
    contagem.columns = ["Técnico", "Quantidade"]

    if not contagem.empty:
        fig = px.pie(
            contagem,
            names="Técnico",
            values="Quantidade",
            hole=0.3,
            color_discrete_sequence=["#1f77b4", "#ff7f0e"]
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum chamado para o técnico selecionado.")

    # =========================================================
    # 6. PRAZO CRÍTICO (com filtro)
    # =========================================================
    st.subheader("Chamados com Prazo Crítico")
    df_critico = df_filtrado[df_filtrado["Geral_Numerico"] <= 2].copy()

    if not df_critico.empty:
        tabela = df_critico[["Id", "Data Criação", "Técnico", "Dias Restantes Geral"]].copy()
        tabela["Data Criação"] = pd.to_datetime(tabela["Data Criação"], errors="coerce").dt.strftime("%d/%m/%Y")
        st.dataframe(tabela, use_container_width=True)
    else:
        st.success("Nenhum chamado com prazo crítico (≤2 dias no Geral)")

    # =========================================================
    # 7. TABELA COMPLETA (com filtro)
    # =========================================================
    st.subheader("Todos os Chamados")
    df_todos = df_filtrado[["Id", "Data Criação", "Técnico", "Dias Restantes Geral"]].copy()
    df_todos["Data Criação"] = pd.to_datetime(df_todos["Data Criação"], errors="coerce").dt.strftime("%d/%m/%Y")
    df_todos = df_todos.sort_values("Id", ascending=False)
    st.dataframe(df_todos, use_container_width=True)