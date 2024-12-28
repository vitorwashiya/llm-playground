import streamlit as st
from views.llm_playground import llm_playground
from views.upload_files import upload_files
from views.create_knowledge_base import create_knowledge_base


def main():
    st.sidebar.title('Menu')
    page = st.sidebar.selectbox(
        'Selecionar Página',
        ['LLM Playground', 'Upload de Arquivos', 'Criar Base de Conhecimento'])

    if page == 'LLM Playground':
        llm_playground()
    elif page == 'Upload de Arquivos':
        upload_files()
    elif page == 'Criar Base de Conhecimento':
        create_knowledge_base()


if __name__ == "__main__":
    main()
