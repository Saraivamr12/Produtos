import streamlit as st
import pandas as pd
import pipefy_api  # Importa o módulo com a função de API

# Configuração do Streamlit
st.set_page_config(page_title="Dashboard Pipefy", layout="wide")

# Título do App
st.title("Dashboard Pipefy")

# Variáveis para simular um login e senha (por questões de segurança, recomendo usar algo mais seguro em produção)
USERNAME = "admin"
PASSWORD = "1234"

# Inicializar session_state para controle de login
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Caixa de login
if not st.session_state.authenticated:
    st.sidebar.title("Login")

    username_input = st.sidebar.text_input("Usuário")
    password_input = st.sidebar.text_input("Senha", type="password")

    # Verificação do login
    if st.sidebar.button("Entrar"):
        if username_input == USERNAME and password_input == PASSWORD:
            st.session_state.authenticated = True
            st.sidebar.success("Login bem-sucedido!")
        else:
            st.sidebar.error("Usuário ou senha incorretos. Tente novamente.")

# Se autenticado, exibir o conteúdo principal
if st.session_state.authenticated:
    # Entrada para o ID da tabela (Database)
    database_id = st.text_input("Digite o ID da tabela que você deseja consultar:")

    # Botão para buscar os registros
    if st.button("Buscar Dados"):
        if database_id:
            st.write(f"Buscando registros para a tabela com ID: {database_id}...")

            # Use o nome correto da função
            try:
                registros = pipefy_api.buscar_todos_registros(database_id)

                # Exibir os registros retornados
                if registros:
                    st.success(f"Encontrados {len(registros)} registros.")
                    df = pd.DataFrame(registros)
                    st.write("### Dados da Tabela:")
                    st.dataframe(df)
                else:
                    st.warning("Nenhum registro encontrado ou houve um erro na consulta.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao buscar os registros: {str(e)}")
        else:
            st.error("Por favor, insira o ID da tabela.")
else:
    st.warning("Por favor, faça login para acessar o dashboard.")
