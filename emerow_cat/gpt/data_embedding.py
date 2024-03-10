from langchain_google_vertexai import VertexAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import getpass
import os


def data_embedding():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

    credential = os.path.join(
        parent_dir, r'gpt/credential.json')
    with open(credential, 'r') as file:
        # Read the contents of the file
        key = file.read()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential
    # if "GOOGLE_API_KEY" not in os.environ:
    #     os.environ["GOOGLE_API_KEY"] = getpass.getpass(key)

    email_data_new = os.path.join(
        parent_dir, r'gpt/email_data.txt')
    file_path = email_data_new
    # Step 1. Load
    loader = TextLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=10)
    texts = text_splitter.split_documents(documents)

    embeddings = VertexAIEmbeddings(model_name='textembedding-gecko@003')

    db = os.path.join(
        parent_dir, r'gpt/emb_db')
    persist_directory = db
    db = Chroma.from_documents(
        documents=documents, embedding=embeddings, persist_directory=persist_directory)
    print('Data embedding complete!')
