import warnings
from langchain_google_vertexai import VertexAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import time

import os
import json
from pathlib import Path

start_time = time.time()
# Store the path to a service account JSON file as the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emerow_cat\gpt\gen-lang-client-0071164010-e2ee8d656ec2.json'

# embedding model and vector databse must be same i.e. 'textembedding-gecko@003'


def email_knowledge_base(question):
    embeddings = VertexAIEmbeddings(model_name='textembedding-gecko@003')
    persist_directory = 'emerow_cat/gpt/gemini_db'
    db = Chroma(persist_directory=persist_directory,
                embedding_function=embeddings)

    # prompt_template = """As a email assistant, you will be presented with information about user's email inbox and outbox. Your task is to provide the most effective response to the user based on established best practices.

    # Here are the questions and related best practices for responding:
    # {context}

    # Question from the user:
    # {question}

    prompt_template = """As an personal assistant, you will be presented with information about someone. Your task is to learn about this person and answer questions about this person.

    Here are the questions and related best practices for responding:
    {context}

    Question from the user:  
    {question}
    """
    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)
    llm = VertexAI(model_name="gemini-pro", temperature=0)
    retriever = db.as_retriever(search_kwargs={"k": 1})
    qa_chain = RetrievalQA.from_chain_type(llm,
                                           chain_type="stuff",
                                           retriever=retriever,
                                           return_source_documents=True,
                                           chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})

    answer = qa_chain(question)
    global question_end_time
    question_end_time = time.time()
    return answer.get('result')


def data_embedding():
    file_path = r"C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emerow_cat\gpt\email_data2.txt"
    # Step 1. Load
    loader = TextLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embeddings = VertexAIEmbeddings(model_name='textembedding-gecko@003')
    persist_directory = 'emerow_cat/gpt/gemini_db'
    db = Chroma.from_documents(
        documents=documents, embedding=embeddings, persist_directory=persist_directory)
    global embeddings_end_time
    embeddings_end_time = time.time()
    print('Data embedding complete!')


# warnings.filterwarnings("ignore", category=DeprecationWarning)


if __name__ == '__main__':
    # data_embedding()
    # embedding_time = embeddings_end_time - start_time
    # print(embedding_time)
    q = 'how old is serena?'
    a = email_knowledge_base(question=q)
    question_time = question_end_time - start_time
    print(question_time)
    print(a)

# 15 seconds
