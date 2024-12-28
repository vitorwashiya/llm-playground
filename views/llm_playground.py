import streamlit as st
import time
import uuid
from handlers.llm_handler import LLMHandler
from utils.file_utils import list_folder
from utils.file_utils import create_directories
from utils.env import list_modelos
from utils.model_info import get_model_info

create_directories(['files', 'faiss'], list_modelos)


def llm_playground():
    st.title('LLM Playground')
    st.sidebar.title('Parâmetros da LLM')

    # Track previous selections to detect changes
    if 'prev_model' not in st.session_state:
        st.session_state.prev_model = None
    if 'prev_knowledge_base' not in st.session_state:
        st.session_state.prev_knowledge_base = None

    model = st.sidebar.selectbox('Selecionar Modelo', list_modelos)
    model_info = get_model_info(model)
    st.sidebar.markdown(f"### Informações do Modelo\n{model_info}")
    model_name = model.replace(":", "_").replace(".", "_")
    knowledge_bases = ['None'] + list_folder(f'faiss/{model_name}')
    selected_knowledge_base = st.sidebar.selectbox('Base de Conhecimento',
                                                   knowledge_bases)

    # Clear history if model or knowledge base changes
    if (model != st.session_state.prev_model or
            selected_knowledge_base != st.session_state.prev_knowledge_base):
        st.session_state.history = []
        st.session_state.prev_model = model
        st.session_state.prev_knowledge_base = selected_knowledge_base

    temperature = st.sidebar.slider('Temperatura', 0.0, 1.0, 0.5)
    top_k = st.sidebar.number_input('Top K', min_value=0, value=100)
    top_p = st.sidebar.number_input('Top P',
                                    min_value=0.0,
                                    max_value=1.0,
                                    value=0.8)
    num_predict = st.sidebar.number_input('Número de Tokens',
                                          min_value=1,
                                          value=1024)

    if 'history' not in st.session_state:
        st.session_state.history = []

    if 'input_key' not in st.session_state:
        st.session_state.input_key = str(uuid.uuid4())

    # Display chat history
    st.subheader('Chat')
    chat_container = st.container()
    with chat_container:
        for interaction in st.session_state.history:
            st.markdown(
                f"<div style='text-align: right; background-color: #DCF8C6; color: #000; padding: 10px; border-radius: 10px; margin: 5px 0;'><b>Você:</b> {interaction['input']}</div>",
                unsafe_allow_html=True)
            st.markdown(
                f"<div style='text-align: left; background-color: #F1F0F0; color: #000; padding: 10px; border-radius: 10px; margin: 5px 0;'><b>LLM:</b> {interaction['response']}</div>",
                unsafe_allow_html=True)
            st.markdown("---")

    # Use a placeholder for the input field
    input_placeholder = st.empty()
    user_input = input_placeholder.text_input('Digite sua mensagem:',
                                              key=st.session_state.input_key)

    if st.button('Enviar'):
        llm_handler = LLMHandler(model, temperature, top_k, top_p, num_predict,
                                 selected_knowledge_base,
                                 st.session_state.history)
        response = llm_handler.get_response(user_input)

        st.session_state.history.append({
            "input": user_input,
            "response": response
        })

        # Generate a new unique key for the next input
        st.session_state.input_key = str(uuid.uuid4())

        # Clear input field by re-rendering it with an empty value
        input_placeholder.text_input('Digite sua mensagem:',
                                     value='',
                                     key=st.session_state.input_key)

        st.rerun()
