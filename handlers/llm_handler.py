from langchain_ollama import ChatOllama
import os
from langchain.globals import set_debug
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st

set_debug(True)


class LLMHandler:
    def __init__(self,
                 model="llama3.1:8b",
                 temperature=0,
                 top_k=None,
                 top_p=None,
                 num_predict=None,
                 knowledge_base=None,
                 history=None):
        self.model = ChatOllama(model=model,
                                temperature=temperature,
                                top_k=top_k,
                                top_p=top_p,
                                num_predict=num_predict)
        self.knowledge_base = knowledge_base if knowledge_base != 'None' else None
        self.model_name = model.replace(":", "_").replace(".", "_")
        self.history = history if history is not None else []

    def get_response(self, input_text):
        try:
            # Combine the last 5 messages from history with current input
            recent_history = self.history[-5:]
            combined_input = "\n".join([
                f"Q: {h['input']}\nA: {h['response']}" for h in recent_history
            ])
            combined_input += f"\nQ: {input_text}\nA:"

            if self.knowledge_base:
                embeddings = OllamaEmbeddings(model=self.model.model)
                db = FAISS.load_local(
                    f"faiss/{self.model_name}/{self.knowledge_base}",
                    embeddings,
                    allow_dangerous_deserialization=True)
                qa_chain = RetrievalQA.from_chain_type(
                    self.model, retriever=db.as_retriever())
                response = qa_chain.invoke({"query": combined_input})
                return response.get("result")
            else:
                response = self.model.invoke(combined_input)
                return response.content
        except Exception as e:
            st.error(f"Erro ao obter resposta do modelo: {e}")
            return None

    def create_knowledge_base(self, vectorstore_name, selected_files):
        try:
            pdf_folder = "files"
            carregadores = [
                PyPDFLoader(os.path.join(pdf_folder, file))
                for file in selected_files
            ]

            documentos = []
            for carregador in carregadores:
                documentos.extend(carregador.load())

            quebrador = CharacterTextSplitter(chunk_size=1000,
                                              chunk_overlap=200)
            textos = quebrador.split_documents(documentos)

            embeddings = OllamaEmbeddings(model=self.model.model)

            with st.spinner('Criando base de conhecimento...'):
                db = FAISS.from_documents(textos, embeddings)
            db.save_local(f"faiss/{self.model_name}/{vectorstore_name}")

            st.success(
                f"Base de conhecimento '{vectorstore_name}' criada com sucesso!"
            )
        except Exception as e:
            st.error(f"Erro ao criar base de conhecimento: {e}")
