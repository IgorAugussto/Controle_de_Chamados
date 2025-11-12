# app.py (raiz)
import streamlit as st
<<<<<<< HEAD
<<<<<<< Updated upstream
from views.dashboard_view import mostrar_dashboard
from services.data_service import carregar_excel
=======
import pandas as pd
from services.data_service import preparar_dados, carregar_planilha_google, get_google_credentials
from views.dashboard_view import mostrar_dashboard
from views.dashboard_aguardando import mostrar_dashboard_aguardando
>>>>>>> Stashed changes
=======
import pandas as pd
from services.data_service import preparar_dados
from views.dashboard_view import mostrar_dashboard
>>>>>>> 733083d527a277d706c3a66a66fce4d5612a83ba

st.set_page_config(page_title="Controle de Chamados - ApoioTech", layout="wide")

# ===== SIDEBAR =====
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/906/906343.png", width=80)
<<<<<<< HEAD
<<<<<<< Updated upstream
st.sidebar.title("Menu")
escolha = st.sidebar.radio("Selecione uma opção", ["Dashboard", "Sobre"])
=======
st.sidebar.title("Dashboard de Chamados")
st.sidebar.success("✅ Dados fictícios carregados automaticamente!")
st.sidebar.info("Recarregue a página se quiser testar com outro arquivo")
>>>>>>> 733083d527a277d706c3a66a66fce4d5612a83ba

# ===== CARREGA DADOS FIXOS (FÁCIL E RÁPIDO) =====
try:
    # ARQUIVO FIXO FICTÍCIO (já está no repo)
    df_raw = pd.read_excel("teste_portfolio/Chamados Geral - API Periodo (teste).xlsx")
    df_raw.columns = df_raw.columns.str.strip().str.replace("Column1.", "", regex=False)
    df_raw.columns = df_raw.columns.str.title().str.strip()
    df = preparar_dados(df_raw)
    
    st.sidebar.success("Arquivo fictício carregado com sucesso! (2.407 chamados)")
    
except Exception as e:
    st.error("Arquivo não encontrado. Rode o gerar_dados_ficticios.py primeiro!")
    st.stop()

<<<<<<< HEAD
if __name__ == "__main__":
    main()
=======
st.sidebar.title("Dashboard de Chamados")
st.sidebar.title("Menu")
st.sidebar.success("✅ Dados fictícios carregados automaticamente!")
st.sidebar.info("Recarregue a página se quiser testar com outro arquivo")

# Menu com abas no topo
tab1, tab2 = st.tabs(["Dashboard Geral", "Dashboard Aguardando Aceite"])

# ===== CARREGA DADOS FIXOS (FÁCIL E RÁPIDO) =====
try:
    df_raw = pd.read_excel("teste_portfolio/Chamados Geral - API Periodo (teste).xlsx")
    df_raw.columns = df_raw.columns.str.strip().str.replace("Column1.", "", regex=False)
    df_raw.columns = df_raw.columns.str.title().str.strip()
    df = preparar_dados(df_raw)
    st.sidebar.success("Arquivo fictício carregado com sucesso! (2.407 chamados)")
except Exception as e:
    st.error("Arquivo não encontrado. Rode o gerar_dados_ficticios.py primeiro!")
    st.stop()

=======
>>>>>>> 733083d527a277d706c3a66a66fce4d5612a83ba
# ===== OPCIONAL: upload pra quem quiser testar outro arquivo =====
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Ou suba seu próprio Excel", type=["xlsx"])
if uploaded_file is not None:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip().str.replace("Column1.", "", regex=False)
    df_raw.columns = df_raw.columns.str.title().str.strip()
    df = preparar_dados(df_raw)
    st.sidebar.success("Seu arquivo foi carregado!")

<<<<<<< HEAD
# ===== MOSTRA DASHBOARDS NAS ABAS =====
with tab1:
    mostrar_dashboard(df)

with tab2:
    # Conecta ao Google Sheets
    gc = get_google_credentials()
    if gc:
        df_aguardando = carregar_planilha_google(gc)
        if df_aguardando is not None:
            mostrar_dashboard_aguardando(df_aguardando)
        else:
            st.error("Não foi possível carregar os dados do Google Sheets.")
    else:
        st.error("Credenciais do Google não encontradas.")
>>>>>>> Stashed changes
=======
# ===== MOSTRA O DASHBOARD =====
mostrar_dashboard(df)
>>>>>>> 733083d527a277d706c3a66a66fce4d5612a83ba
