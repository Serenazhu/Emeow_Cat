# from refresh_data_prep import add_data
import refreshed_data_prep
import first_data_prep
import data_embedding
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
import subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Construct the path to the file in the parent directory

credential = os.path.join(
    parent_dir, r'gpt/credential.json')
# st.set_page_config(page_title='Google PalM 2', layout='wide')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential
email_data = os.path.join(
    parent_dir, r'gpt/email_data.txt')


def refresh():
    vectorstore = read_data()
  # new data
    file_path = email_data
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


current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Construct the path to the file in the parent directory

db = os.path.join(
    parent_dir, r'gpt/emb_db')


def read_data():
    embeddings = VertexAIEmbeddings(model_name='textembedding-gecko@003')
    # 'C:/Users/Leo/OneDrive - CBRE, Inc/Documents/Python AI Projects/TM1 AI Assistant Project/palm_db'
    persist_directory = db
    store = Chroma(persist_directory=persist_directory,
                   embedding_function=embeddings)
    return store


def gen_answer(question):
    prompt_template = """As an email assistant, you will be presented with someone's inbox and outbox.

    Here are the all the emails:
    {context}

    Question from the user:  
    {question}

    Please provide the most suitable response to be sent to the user. If the recommended response is irrelevant, please make it clear that the answer is from Google PaLM own knowledge.
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
    answer = qa_chain(question)
    return answer


def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0


st.set_page_config(page_title="Mimi", page_icon=":cat:")
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))


if st.sidebar.button('Refresh'):
    refreshed_data_prep.data_prep_2()
    refresh()


# Construct the path to the file in the parent directory


email_data = os.path.join(
    parent_dir, r'gpt/email_data.txt'
)

if st.sidebar.button('first time'):
    if is_file_empty(email_data):
        first_data_prep.data_prep_1()
        data_embedding.data_embedding()

c1, c2 = st.columns([4, 1])
with c1:
    st.subheader("Mimi :cat:")


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
        st.write("Analyzing your emails...")
        result = gen_answer(prompt)
        st.session_state['msg'].append(
            {'role': 'assistant', 'content': result.get('result')})
        st.info(result.get('result'))

        # st.divider()
        # page_content_value = result['source_documents'][0].page_content
        # st.caption('Reference :books:')
        # st.markdown(page_content_value)

# streamlit run "C:\Users\Leo\OneDrive - CBRE, Inc\Documents\Python AI Projects\PostgreSQL DB\TM1 AI Assistant Project\tm1_ai_palm.py"
 # streamlit run "TM1 AI Assistant Project\pages\tm1_ai_PaLM.py"

# streamlit run "C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emerow_cat\gpt\mimi.py"
