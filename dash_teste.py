import streamlit as st
import pandas as pd
import pipefy_api  # Importa o módulo com a função de API

# Configuração do Streamlit
st.set_page_config(page_title="Dashboard Pipefy", layout="wide")

# Título do App
st.title("Dashboard Pipefy")

# Entrada para o ID da tabela (Database)
database_id = st.text_input("Digite o ID da tabela que você deseja consultar:")

# Botão para buscar os registros
if st.button("Buscar Dados"):
    if database_id:
        st.write(f"Buscando registros para a tabela com ID: {database_id}...")

        # Use o nome correto da função
        registros = pipefy_api.buscar_todos_registros(database_id)

        # Exibir os registros retornados
        if registros:
            st.success(f"Encontrados {len(registros)} registros.")
            df = pd.DataFrame(registros)
            st.write("### Dados da Tabela:")
            st.dataframe(df)
        else:
            st.warning("Nenhum registro encontrado ou houve um erro na consulta.")
    else:
        st.error("Por favor, insira o ID da tabela.")
