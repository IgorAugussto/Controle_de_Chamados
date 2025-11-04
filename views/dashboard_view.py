# Camada de apresentação (telas, gráficos, componentes)
# Tudo que é exibido no Streamlit

import streamlit as st
import plotly.express as px

def mostrar_dashboard(df):
    st.title("📊 Dashboard de Chamados")

    # --- KPIs ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Chamados Totais", len(df))
    col2.metric("Abertos", (df["Status"] == "Aberto").sum())
    col3.metric("Fechados", (df["Status"] == "Fechado").sum())

    # --- Filtros ---
    st.sidebar.header("Filtros")
    status_filtro = st.sidebar.selectbox(
           "Filtrar por Status", ["Todos"] + list(df["Status"].unique())
    )
    
    # CORREÇÃO: Remover valores NaN antes de criar o filtro
    prioridades_disponiveis = df["Priority"].dropna().unique()
    prioridade_filtro = st.sidebar.multiselect(
        "Filtrar por Prioridade", 
        prioridades_disponiveis, 
        default=prioridades_disponiveis
    )

    # Aplicar filtros
    if status_filtro != "Todos":
        df = df[df["Status"] == status_filtro]
    
    # CORREÇÃO: Incluir também registros com Priority vazia se nenhum filtro foi selecionado
    if prioridade_filtro:
        df = df[df["Priority"].isin(prioridade_filtro)]

    st.divider()

    #--- Gráfico por Prioridade ---
    # CORREÇÃO: Remover NaN antes de plotar
    df_prioridade = df[df["Priority"].notna()]
    if not df_prioridade.empty:
        fig1 = px.bar(
            df_prioridade,
            x="Priority",
            color="Status",
            title="Chamados por Prioridade e Status",
            barmode="group",
            text_auto=True
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Nenhum chamado com prioridade definida")

    #--- Gráfico por Tipo de Chamado ---
    if "Tickettype" in df.columns:
        df_tipo = df[df["Tickettype"].notna()]
        if not df_tipo.empty:
            fig2 = px.pie(df_tipo, names="Tickettype", title="Distribuição por Tipo de Chamado")
            st.plotly_chart(fig2, use_container_width=True)

    # --- SLA ---
    if "Dias Restantes" in df.columns:
        st.subheader("⏳ Chamados com Prazo Crítico")
        df_vencendo = df[df["Dias Restantes"] <= 2]
        if not df_vencendo.empty:
            st.dataframe(df_vencendo[["Id", "Priority", "Status", "Dias Restantes"]])
        else:
            st.success("✅ Nenhum chamado próximo do vencimento")

    # --- Tabela completa ---
    st.subheader("📋 Chamados Recentes")
    st.dataframe(df.tail(15))