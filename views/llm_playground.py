import streamlit as st
from handlers.llm_handler import LLMHandler
from utils.file_utils import list_folder
from utils.file_utils import create_directories
from utils.env import list_modelos

create_directories(['files', 'faiss'], list_modelos)


def llm_playground():
    st.title('LLM Playground')
    st.sidebar.title('Parâmetros da LLM')
    model = st.sidebar.selectbox('Selecionar Modelo', list_modelos)
    model_name = model.replace(":", "_").replace(".", "_")
    temperature = st.sidebar.slider('Temperatura', 0.0, 1.0, 0.5)
    top_k = st.sidebar.number_input('Top K', min_value=0, value=100)
    top_p = st.sidebar.number_input('Top P',
                                    min_value=0.0,
                                    max_value=1.0,
                                    value=0.8)
    num_predict = st.sidebar.number_input('Número de Tokens',
                                          min_value=1,
                                          value=1024)
    knowledge_bases = ['None'] + list_folder(f'faiss/{model_name}')
    selected_knowledge_base = st.sidebar.selectbox('Base de Conhecimento',
                                                   knowledge_bases)

    user_input = st.text_area('Entrada da LLM:', height=200)

    if st.button('Run LLM'):
        llm_handler = LLMHandler(model, temperature, top_k, top_p, num_predict,
                                 selected_knowledge_base)
        response = llm_handler.get_response(user_input)
        st.write(response)
