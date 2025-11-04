import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_dashboard(df):

    st.write("### 🧩 Pré-visualização do DataFrame")
    st.dataframe(df.head(10))
    st.write("Shape (linhas, colunas):", df.shape)
    st.write("Colunas:", list(df.columns))

    st.title("📊 Dashboard de Chamados")

    # --- KPIs ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Chamados Totais", len(df))
    col2.metric("Abertos", (df["status"] == "Aberto").sum())
    col3.metric("Fechados", (df["status"] == "Fechado").sum())

    # --- Filtros ---
    st.sidebar.header("Filtros")
    
    st.write("### Linhas após filtros:", len(df))


    # 🔧 Removendo valores NaN antes de usar nas opções
    status_opcoes = sorted(df["status"].dropna().unique())
    prioridade_opcoes = sorted(df["priority"].dropna().unique())

    status_filtro = st.sidebar.selectbox(
        "Filtrar por Status", ["Todos"] + status_opcoes
    )

    prioridade_filtro = st.sidebar.multiselect(
        "Filtrar por Prioridade",
        options=prioridade_opcoes,
        default=prioridade_opcoes  # ✅ agora só valores válidos
    )

    if status_filtro != "Todos":
        df = df[df["status"] == status_filtro]
    df = df[df["priority"].isin(prioridade_filtro)]

    st.divider()

    # --- Gráfico por prioridade ---
    fig1 = px.bar(
        df,
        x="priority",
        color="status",
        title="Chamados por Prioridade e Status",
        barmode="group",
        text_auto=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- SLA ---
    st.subheader("⏳ Chamados com Prazo Crítico (≤ 2 dias)")
    df_vencendo = df[df["Dias Restantes"] <= 2]
    st.dataframe(df_vencendo[["id", "priority", "status", "Dias Restantes"]])

    # --- Tabela completa ---
    st.subheader("📋 Chamados Recentes")
    st.dataframe(df.tail(15))
