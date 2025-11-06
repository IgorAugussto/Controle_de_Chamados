import streamlit as st
import pandas as pd
from services.data_service import carregar_dados, preparar_dados
from views.dashboard_view import mostrar_dashboard

# ===== CONFIGURAÇÃO DA PÁGINA =====
st.set_page_config(page_title="Controle de Chamados - ApoioTech", layout="wide")

# ===== SIDEBAR COM LOGO E MENU =====
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/906/906343.png", width=80)
st.sidebar.title("Menu")
escolha = st.sidebar.radio("Selecione uma opção", ["Dashboard", "Sobre"])

# ===== FUNÇÃO PARA CARREGAR DADOS COM UPLOAD =====
def carregar_com_upload():
    st.sidebar.header("Upload do Excel")
    uploaded_file = st.sidebar.file_uploader(
        "Arraste ou clique para subir o arquivo Excel",
        type=["xlsx", "xls"],
        help="Arquivo: Chamados Geral - API Periodo.xlsx"
    )

    if uploaded_file is not None:
        try:
            # Lê direto do upload
            df_raw = pd.read_excel(uploaded_file)
            # Limpa colunas (mesmo código que você já tinha)
            df_raw.columns = df_raw.columns.str.strip().str.replace("Column1.", "", regex=False)
            df_raw.columns = df_raw.columns.str.title().str.strip()
            return preparar_dados(df_raw)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            return None
    else:
        st.warning("Aguardando upload do arquivo Excel...")
        st.info("👆 Use o campo na barra lateral para subir o Chamados Geral - API Periodo.xlsx")
        return None

# ===== MAIN =====
def main():
    if escolha == "Dashboard":
        df = carregar_com_upload()
        if df is not None:
            mostrar_dashboard(df)
        else:
            st.stop()  # Para a execução até ter dados

    elif escolha == "Sobre":
        st.title("ℹ️ Sobre o Projeto")
        st.write("""
        **Dashboard de Chamados - ApoioTech**  
        Criado para análise rápida de SLA, prioridades e tipos de chamado.  
        Agora funciona 100% online — basta subir o Excel atualizado!
        """)
        st.success("App atualizado com upload de arquivo (nunca mais FileNotFound!)")

if __name__ == "__main__":
    main()