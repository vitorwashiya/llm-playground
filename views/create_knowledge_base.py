import streamlit as st
from handlers.llm_handler import LLMHandler
from utils.file_utils import list_pdf_files
from utils.env import list_modelos


def create_knowledge_base():
    st.title('Criar Base de Conhecimento')
    st.subheader('Selecione os arquivos para compor a base de conhecimento:')
    model = st.selectbox('Selecionar Modelo', list_modelos)
    files = list_pdf_files('files')
    selected_files = st.multiselect('Arquivos disponíveis:', files)
    knowledge_base = st.text_input('Nome da Base de Conhecimento:')

    if st.button('Criar'):
        if not knowledge_base:
            st.error('Por favor, insira um nome para a base de conhecimento.')
        elif not selected_files:
            st.error('Por favor, selecione pelo menos um arquivo.')
        else:
            llm_handler = LLMHandler(model)
            llm_handler.create_knowledge_base(knowledge_base, selected_files)
            st.write(
                f"Base de conhecimento '{knowledge_base}' criado com sucesso com os arquivos: {', '.join(selected_files)}"
            )
