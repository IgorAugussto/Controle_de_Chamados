import streamlit as st
from views.dashboard_view import mostrar_dashboard
from services.data_service import carregar_excel

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

    # Tenta recuperar df já carregado na sessão
    df = st.session_state.get("df_cache", None)

    # Se o usuário fez um upload novo, processa e guarda na sessão
    if uploaded_file is not None:
        try:
            df = carregar_excel(uploaded_file)  # usa a função cacheada do service
            st.session_state.df_cache = df       # persiste para manter após reload
            st.success("✔ Dados carregados com sucesso!")
            # opcional: guardar metadados do arquivo
            st.session_state.upload_name = getattr(uploaded_file, "name", "arquivo.xlsx")
            return df
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            return None

    # Se não tem upload na vez, mas existe cache na sessão -> retorna df
    if df is not None:
        # Aqui não mostramos o uploader como "preenchido", mas usamos os dados
        return df

    # Se não tem nada
    st.warning("Aguardando upload do arquivo Excel...")
    st.info("👆 Use o campo na barra lateral para subir o arquivo")
    return None

# ===== MAIN =====
def main():
    df = carregar_com_upload()
    
    if df is not None:
        mostrar_dashboard(df)

if __name__ == "__main__":
    main()