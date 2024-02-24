from langchain_google_vertexai import VertexAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import time
import os
import streamlit as st


# st.set_page_config(page_title='Google PalM 2', layout='wide')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emerow_cat\gpt\gen-lang-client-0071164010-e2ee8d656ec2.json'


# def data_embedding():
#     file_path = r"C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emerow_cat\gpt\email_data2.txt"
#     # Step 1. Load
#     loader = TextLoader(file_path)
#     documents = loader.load()

#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000, chunk_overlap=10)
#     texts = text_splitter.split_documents(documents)

#     embeddings = VertexAIEmbeddings(model_name='textembedding-gecko@003')
#     persist_directory = r'C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emerow_cat\test_db'
#     db = Chroma.from_documents(
#         documents=documents, embedding=embeddings, persist_directory=persist_directory)
#     print('Data embedding complete!')


def add_doc():
    vectorstore = read_data()
  # new data
    file_path = r"C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emerow_cat\gpt\email_data2.txt"
    # Step 1. Load
    loader = TextLoader(file_path)
    documents = loader.load()
    # Step 2. Split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=10)
    texts = text_splitter.split_documents(documents)

    # Load and embed new documents
    vectorstore.add_documents(texts)
    # Persist the changes
    vectorstore.persist()
    print('Data add complete!')


def read_data():
    embeddings = VertexAIEmbeddings(model_name='textembedding-gecko@003')
    # 'C:/Users/Leo/OneDrive - CBRE, Inc/Documents/Python AI Projects/TM1 AI Assistant Project/palm_db'
    persist_directory = r'C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emerow_cat\gpt\test_db'
    store = Chroma(persist_directory=persist_directory,
                   embedding_function=embeddings)
    return store


def gen_answer(question):
    prompt_template = """As a personal assistant, you will be presented with someone's self introduction

    Here are the info about that person:
    {context}

    Question from the user:  
    {question}

    Please provide the most suitable response to be sent to the user. If the recommended response is irrelevant, please make it clear that the answer is from Google PaLM own knowledge.
    Always say "Happy querying! 😊" at the end of the answer.
    """
    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)

    db = read_data()
    llm = VertexAI(model_name="gemini-pro", temperature=0)

    retriever = db.as_retriever(search_kwargs={"k": 1})

    qa_chain = RetrievalQA.from_chain_type(llm,
                                           chain_type="stuff",
                                           retriever=retriever,
                                           return_source_documents=True,
                                           chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    # answer=qa_chain.run(question)
    answer = qa_chain(question)
    return answer


st.set_page_config(page_title="Mimi", page_icon=":cat:")
if st.sidebar.button('Refresh'):
    add_doc()

c1, c2 = st.columns([4, 1])
with c1:
    st.subheader("Mimi :cat:")
# with c2:
#     img=Image.open(r'D:\LZhu Documents\Python Program\cbre.png')
#     img=st.image(img)

# Chat History List
# Intialization key='msg'
if 'msg' not in st.session_state:
    st.session_state['msg'] = []

# to present historical chat msg
for msg in st.session_state['msg']:
    if isinstance(msg, dict):
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

# message = st.text_area("Question")
prompt = st.chat_input("Ask me anything about your email...")
# if st.button('Answer'):
if prompt:
    # add data to session_state
    st.session_state['msg'].append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    with st.chat_message('assistant'):
        st.write("Generating best practice message...")
        result = gen_answer(prompt)
        st.session_state['msg'].append(
            {'role': 'assistant', 'content': result.get('result')})
        st.info(result.get('result'))

        st.divider()
        page_content_value = result['source_documents'][0].page_content
        st.caption('Source Documents :books:')
        st.markdown(page_content_value)

# streamlit run "C:\Users\Leo\OneDrive - CBRE, Inc\Documents\Python AI Projects\PostgreSQL DB\TM1 AI Assistant Project\tm1_ai_palm.py"
 # streamlit run "TM1 AI Assistant Project\pages\tm1_ai_PaLM.py"
