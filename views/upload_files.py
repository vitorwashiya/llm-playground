import streamlit as st
import os
from utils.file_utils import list_pdf_files


def upload_files():
    st.title('Upload de Arquivos:')
    st.subheader('Arquivos disponíveis:')

    # Search functionality
    search_query = st.text_input('Buscar Arquivos:')

    files = list_pdf_files('files')
    if search_query:
        files = [
            file for file in files if search_query.lower() in file.lower()
        ]

    cols = st.columns(3)
    for i, file in enumerate(files):
        file_path = os.path.join('files', file)
        with cols[i % 3]:
            st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; position: relative;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/8/87/PDF_file_icon.svg" alt="{file}" style="width: 100%; height: auto; border-radius: 5px;">
                    <p style="text-align: center;">{file}</p>
                </div>
            """,
                        unsafe_allow_html=True)
            if st.button(f'Delete', key=file, use_container_width=True):
                os.remove(file_path)
                st.rerun()

    uploaded_file = st.file_uploader("Escolha um arquivo PDF para upload:",
                                     type="pdf")
    if uploaded_file is not None:
        save_path = os.path.join('files', uploaded_file.name)
        with open(save_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.write("Upload de arquivo foi bem sucedido!")
        st.write(f"Arquivo salvo em {save_path}")
        st.rerun()
