import google.generativeai as palm
from langchain.embeddings.google_palm import GooglePalmEmbeddings
from langchain.llms.google_palm import GooglePalm
# from langchain.vectorstores import Chroma
# from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import streamlit as st
import sqlite3

# st.set_page_config(page_title='Google PalM 2', layout='wide')
# st.set_page_config(page_title="email Assistant", page_icon=":ice_cube:")


api_key = 'AIzaSyAruTX3FHGoGOv7PaeKTOA0mjSuMAPDxz0'
palm.configure(api_key=api_key)


def prep_data():
    Businesses = {}
    Representatives = {}
    Inbox = {}
    Sent = {}
    conn = sqlite3.connect(
        r'C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emaildb.db')
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()
    cursor4 = conn.cursor()
    cursor5 = conn.cursor()
    # Business
    cursor1.execute(
        'SELECT Company FROM Businesses')
    companies = cursor1.fetchall()
    cursor2.execute(
        'SELECT Type FROM Businesses')
    types = cursor1.fetchall()

    for company, type in zip(companies, types):
        Businesses[company] = type

    # Representatives
    cursor1.execute(
        'SELECT Reps FROM Representatives')
    cursor2.execute(
        'SELECT Email FROM Representatives')
    cursor3.execute(
        'SELECT Company FROM Representatives')
    reps = cursor1.fetchall()
    emails = cursor2.fetchall()
    companies = cursor3.fetchall()
    ns = 1
    for rep, email, company, n in zip(reps, emails, companies, range(ns)):
        Representatives[n] = {}
        Representatives[n]['rep'] = rep
        Representatives[n]['email'] = email
        Representatives[n]['company'] = company

    # Inbox
    cursor1.execute(
        'SELECT Email FROM Inbox')
    cursor2.execute(
        'SELECT Subject FROM Inbox')
    cursor3.execute(
        'SELECT Body FROM Inbox')
    cursor4.execute(
        'SELECT Time FROM Inbox')
    cursor5.execute(
        'SELECT Reps FROM Inbox')

    emails = cursor1.fetchall()
    subjects = cursor2.fetchall()
    bodies = cursor3.fetchall()
    times = cursor4.fetchall()
    reps = cursor5.fetchall()

    ns = 1
    for email, subject, body, time, rep, n in zip(emails, subjects, bodies, times, reps, range(ns)):
        Inbox[n] = {}
        Inbox[n]['email'] = email
        Inbox[n]['subject'] = subject
        Inbox[n]['body'] = body
        Inbox[n]['time'] = time
        Inbox[n]['rep'] = rep

    # Sent
    cursor1.execute(
        'SELECT Email FROM Sent')
    cursor2.execute(
        'SELECT Subject FROM Sent')
    cursor3.execute(
        'SELECT Body FROM Sent')
    cursor4.execute(
        'SELECT Time FROM Sent')

    emails = cursor1.fetchall()
    subjects = cursor2.fetchall()
    bodies = cursor3.fetchall()
    times = cursor4.fetchall()
    reps = cursor5.fetchall()

    ns = 1
    for email, subject, body, time, n in zip(emails, subjects, bodies, times, range(ns)):
        Sent[n] = {}
        Sent[n]['email'] = email
        Sent[n]['subject'] = subject
        Sent[n]['body'] = body
        Sent[n]['time'] = time

    cursor1.close()
    cursor2.close()
    cursor3.close()
    cursor4.close()
    cursor5.close()
    conn.close()

    return Businesses, Representatives, Inbox, Sent


def summary():
    email_dict = []
    Businesses, Representatives, Inbox, Sent = prep_data()
    email_dict.append(Businesses)
    email_dict.append(Representatives)
    email_dict.append(Inbox)
    email_dict.append(Sent)
    print(email_dict)


def load_data():
    # # Step 1. Load
    # loader = CSVLoader(
    #     file_path=r"C:\Users\leo.zhu\OneDrive - CBRE, Inc\Documents\Python AI Projects\TM1 Q&A.csv")
    # documents = loader.load()

    # # Step 2. Split
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=1000, chunk_overlap=10)
    # texts = text_splitter.split_documents(documents)

    # Step 3. Store
    # convert text to embeddings
    embeddings = GooglePalmEmbeddings(google_api_key=api_key)

    # Supplying a persist_directory will store the embeddings on disk
    persist_directory = 'db'
    # db = Chroma.from_documents(
    #     documents=email_dict, embedding=embeddings, persist_directory=persist_directory)

    print('Data load complete!')


def add_doc():
    vectorstore = read_data()

    # loader = CSVLoader(
    #     file_path=r"C:\Users\leo.zhu\OneDrive - CBRE, Inc\Documents\Python AI Projects\TM1 Q&A2.csv")
    # documents = loader.load()
    # # Step 2. Split
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=1000, chunk_overlap=10)
    # texts = text_splitter.split_documents(documents)

    # Load and embed new documents
    # vectorstore.add_documents(email_dict)
    # # Persist the changes
    # vectorstore.persist()
    # print('Data add complete!')


def read_data():
    embeddings = GooglePalmEmbeddings(google_api_key=api_key)
    # 'C:/Users/Leo/OneDrive - CBRE, Inc/Documents/Python AI Projects/TM1 AI Assistant Project/palm_db'
    persist_directory = r"C:\Users\seren\OneDrive\Documents\Emeow_cat\emeow_cat_web\emerow_cat\gpt\vectordb.db"
    store = Chroma(persist_directory=persist_directory,
                   embedding_function=embeddings)
    return store


def gen_answer(question):
    prompt_template = """As a email assistant, you will be presented with common questions and related answers about the user's email. Your task is to provide the most effective response to the user based on established best practices.

    Here are user's emails:
    {context}

    Question from the user:  
    {question}

    Please provide the most suitable response to be sent to the user. If the recommended response is irrelevant, please make it clear that the answer is from Google PaLM own knowledge.
    """
    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)

    db = read_data()
    llm = GooglePalm(google_api_key=api_key)
    llm.temperature = 0

    retriever = db.as_retriever(search_kwargs={"k": 1})

    qa_chain = RetrievalQA.from_chain_type(llm,
                                           chain_type="stuff",
                                           retriever=retriever,
                                           return_source_documents=True,
                                           chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    # answer=qa_chain.run(question)
    answer = qa_chain(question)
    return answer


def streamlit():
    # st.set_page_config(page_title="email Assistant", page_icon=":ice_cube:")
    if st.sidebar.button('Add Docs'):
        add_doc()

    c1, c2 = st.columns([4, 1])
    with c1:
        st.subheader("Email Assistant :hugging_face:")
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
    prompt = st.chat_input("Ask me anything about TM1...")
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


if __name__ == '__main__':
    summary()
