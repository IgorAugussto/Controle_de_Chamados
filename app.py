import streamlit as st
from services.data_service import carregar_dados, preparar_dados
from views.dashboard_view import mostrar_dashboard

def main():
    st.set_page_config(page_title="Controle de Chamados", layout="wide")

    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/906/906343.png", width=80)
    st.sidebar.title("Menu")
    escolha = st.sidebar.radio("Selecione uma opção", ["Dashboard", "Sobre"])

    if escolha == "Dashboard":
        caminho_excel = "data/Chamados Geral - API Periodo.xlsx"
        df = carregar_dados(caminho_excel)
        df = preparar_dados(df)
        mostrar_dashboard(df)

    elif escolha == "Sobre":
        st.title("ℹ️ Sobre o Projeto")
        st.write("""
        Este sistema foi criado para análise de chamados técnicos, com métricas automáticas,
        gráficos interativos e cálculo de SLA.
        """)

if __name__ == "__main__":
    main()
