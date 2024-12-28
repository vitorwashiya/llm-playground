import streamlit as st
from llm import LLM
import os

list_modelos = ['llama3.2:3b', 'llama3.1:8b', 'llama3.3:70b']

for dir in ['files', 'faiss']:
    if not os.path.exists(dir):
        os.makedirs(dir)
for model in list_modelos:
    model_name = model.replace(":", "_").replace(".", "_")
    model_dir = os.path.join('faiss', model_name)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

page = st.sidebar.selectbox('Selecionar Página', ['LLM Playground', 'Upload de Arquivos', 'Criar Base de Conhecimento'])

if page == 'LLM Playground':
    st.title('LLMPlayground')

    st.sidebar.title('Parâmetros da LLM')
    model = st.sidebar.selectbox('Selecionar Modelo', list_modelos)
    model_name = model.replace(":", "_").replace(".", "_")
    temperature = st.sidebar.slider('Temperatura', 0.0, 1.0, 0.0)
    top_k = st.sidebar.number_input('Top K', min_value=0, value=50)
    top_p = st.sidebar.number_input('Top P', min_value=0.0, max_value=1.0, value=0.8)
    num_predict = st.sidebar.number_input('Número de Tokens', min_value=1, value=1024)
    knowledge_bases = ['None'] + [f for f in os.listdir(f'faiss/{model_name}') if os.path.isdir(os.path.join(f'faiss/{model_name}', f))]
    selected_knowledge_base = st.sidebar.selectbox('Base de Conhecimento', knowledge_bases)

    user_input = st.text_area('Entrada da LLM:', height=200)

    if st.button('Run LLM'):
        llm = LLM(model=model, temperature=temperature, top_k=top_k, top_p=top_p, num_predict=num_predict, knowledge_base=selected_knowledge_base)
        response = llm.get_response(user_input)
        st.write(response)

elif page == 'Upload de Arquivos':
    st.title('Upload de Arquivos:')

    st.subheader('Arquivos em uso:')
    files = os.listdir('files')
    cols = st.columns(3)
    for i, file in enumerate(files):
        file_path = os.path.join('files', file)
        with cols[i % 3]:
            st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; position: relative;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/8/87/PDF_file_icon.svg" alt="{file}" style="width: 100%; height: auto; border-radius: 5px;">
                    <p style="text-align: center;">{file}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f'Delete', key=file, use_container_width=True):
                os.remove(file_path)
                st.rerun()
                
    uploaded_file = st.file_uploader("Escolha um arquivo para upload:")
    if uploaded_file is not None:
        save_path = os.path.join('files', uploaded_file.name)
        with open(save_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.write("Upload de arquivo foi bem sucedido!")
        st.write(f"Arquivo salvo em {save_path}")
        uploaded_file = None
        st.rerun()

elif page == 'Criar Base de Conhecimento':
    st.title('Create VectorStore')

    st.subheader('Select files to include in the VectorStore:')
    files = os.listdir('files')
    model = st.selectbox('Selecionar Modelo', list_modelos)
    selected_files = st.multiselect('Arquivos disponíveis:', files)
    vectorstore_name = st.text_input('Nome do VectorStore:')
    
    if st.button('Create VectorStore'):
        if not vectorstore_name:
            st.error('Por favor, insira um nome para o VectorStore.')
        elif not selected_files:
            st.error('Por favor, selecione pelo menos um arquivo.')
        else:
            llm = LLM(model=model)
            llm.create_vectorstore(vectorstore_name, selected_files)
            st.write(f"VectorStore '{vectorstore_name}' criado com sucesso com os arquivos: {', '.join(selected_files)}")
