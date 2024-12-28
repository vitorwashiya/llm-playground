# LLM Playground

Este projeto é uma aplicação baseada em Streamlit que permite aos usuários interagir com vários modelos de linguagem (LLMs), fazer upload de arquivos e criar bases de conhecimento usando bases vetoriais.

## Estrutura do Projeto

```
faiss/
    llama3_1_70b/
    llama3_1_8b/
        KB/
            index.faiss
            index.pkl
    llama3_2_3b/
        KB/
            index.faiss
            index.pkl
files/
llm.py
ui.py
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/seuusuario/LLM-Playground.git
cd LLM-Playground
```

Crie um ambiente virtual e ative-o:

```bash
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
```

Instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

## Executando a Aplicação

Para executar a aplicação Streamlit, use o seguinte comando:

```bash
streamlit run ui.py
```

## Uso

### LLM Playground

1. Selecione a página "LLM Playground" na barra lateral.
2. Configure os parâmetros do LLM, como modelo, temperatura, top_k, top_p e número de tokens.
3. Selecione uma base de conhecimento, se disponível.
4. Insira seu texto de entrada na área de texto fornecida.
5. Clique no botão "Run LLM" para obter a resposta do LLM selecionado.

### Upload de Arquivos

1. Selecione a página "Upload de Arquivos" na barra lateral.
2. Veja os arquivos atuais na pasta `files`.
3. Faça upload de novos arquivos para a pasta `files` usando o uploader de arquivos.
4. Exclua arquivos existentes clicando no botão "Delete" ao lado de cada arquivo.

### Criar Base de Conhecimento

1. Selecione a página "Criar Base de Conhecimento" na barra lateral.
2. Selecione o modelo e os arquivos que deseja incluir na base de vetores.
3. Insira um nome para a base de vetores.
4. Clique no botão "Create VectorStore" para criar a base de vetores com os arquivos selecionados.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request para quaisquer alterações.

## Contato

Para quaisquer perguntas ou sugestões, entre em contato com washiya.hideki@gmail.com.