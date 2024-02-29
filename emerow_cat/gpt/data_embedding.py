from langchain_google_vertexai import VertexAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import time
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'emerow_cat\gpt\gen-lang-client-0071164010-e2ee8d656ec2.json'


def data_embedding():
    file_path = r"emerow_cat\gpt\email_data_new.txt"
    # Step 1. Load
    loader = TextLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=10)
    texts = text_splitter.split_documents(documents)

    embeddings = VertexAIEmbeddings(model_name='textembedding-gecko@003')
    persist_directory = r'emerow_cat\gpt\test_db'
    db = Chroma.from_documents(
        documents=documents, embedding=embeddings, persist_directory=persist_directory)
    print('Data embedding complete!')


data_embedding()
