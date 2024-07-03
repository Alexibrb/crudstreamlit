import streamlit as st
import pandas as pd
import openpyxl


st.set_page_config( page_title="CRUD", layout="wide")

custom_css = """
    <style>
    table {
      width: 100%; /* Define a largura da tabela como 100% do contêiner pai */
      border-collapse: collapse; /* Remove espaçamento entre as células */
    }

    th, td {
      padding: 8px; /* Espaçamento interno das células */
      text-align: left; /* Alinhamento do texto à esquerda */
    }

    th:nth-child(1), td:nth-child(1) {
      width: 10%; /* Ajusta a largura da primeira coluna */
    }

    th:nth-child(2), td:nth-child(2) {
      width: 10%; /* Ajusta a largura da segunda coluna */
    }

    th:nth-child(3), td:nth-child(3) {
      width: 60%; /* Ajusta a largura da terceira coluna */
    }
    </style>
    """

# Funções auxiliares
def read_data():
    return pd.read_excel('database.xlsx')

def write_data(df):
    df.to_excel('database.xlsx', index=False)

# Leitura dos dados
df = read_data()

# Sidebar para navegação
st.sidebar.title("CRUD com Streamlit e Excel")
option = st.sidebar.selectbox("Escolha uma operação", ["Ler os Dados", "Criar Dados", "Atualizar Registro", "Deletar Registro"])


if option == "Ler os Dados":
    st.title("Leitura dos registros")

    # Exibir a tabela com estilo CSS inline
    df_reset = df.reset_index(drop=True)
    st.markdown(custom_css, unsafe_allow_html=True)
    st.table(df_reset)


elif option == "Criar Dados":
    st.title("Adicionar novo registro")
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0, step=1)
    if st.button("Adicionar", disabled=not (nome and idade)):
        new_id = df['ID'].max() + 1 if not df.empty else 1
        new_row = pd.DataFrame({'ID': [new_id], 'Nome': [nome], 'Idade': [idade]})
        df = pd.concat([df, new_row], ignore_index=True)
        write_data(df)

        st.success("Registro adicionado com sucesso!")



elif option == "Atualizar Registro":
    st.title("Atualizar um registro")
    record_id = st.number_input("ID do registro a ser atualizado", min_value=0, step=1)
    if record_id in df['ID'].values:
        nome = st.text_input("Nome", value=df[df['ID'] == record_id]['Nome'].values[0])
        idade = st.number_input("Idade", min_value=0, step=1, value=df[df['ID'] == record_id]['Idade'].values[0])
        if st.button("Atualizar"):
            df.loc[df['ID'] == record_id, 'Nome'] = nome
            df.loc[df['ID'] == record_id, 'Idade'] = idade
            write_data(df)
            st.success("Registro atualizado com sucesso!")
    else:
        st.warning("ID não encontrado!")
        with st.expander("Visualizar Registros"):
            df_reset = df.reset_index(drop=True)
            st.markdown(custom_css, unsafe_allow_html=True)
            st.table(df_reset)

elif option == "Deletar Registro":
    st.title("Excluir um registro")
    record_id = st.number_input("ID do registro a ser excluído", min_value=0, step=1)
    if record_id in df['ID'].values:
        if st.button("Excluir"):
            df = df[df['ID'] != record_id]
            write_data(df)
            st.success("Registro excluído com sucesso!")
    else:
        st.warning("ID não encontrado!")
        with st.expander("Visualizar Registros"):
            df_reset = df.reset_index(drop=True)
            st.markdown(custom_css, unsafe_allow_html=True)
            st.table(df_reset)
