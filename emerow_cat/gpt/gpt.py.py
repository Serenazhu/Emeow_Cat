import google.generativeai as palm
from langchain.embeddings.google_palm import GooglePalmEmbeddings
from langchain.llms.google_palm import GooglePalm
#from langchain.vectorstores import Chroma
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import streamlit as st
from PIL import Image

# st.set_page_config(page_title='Google PalM 2', layout='wide')

api_key = 'AIzaSyAruTX3FHGoGOv7PaeKTOA0mjSuMAPDxz0' 
palm.configure(api_key=api_key)

def load_data():
    #Step 1. Load
    loader = CSVLoader(file_path=r"C:\Users\leo.zhu\OneDrive - CBRE, Inc\Documents\Python AI Projects\TM1 Q&A.csv")
    documents = loader.load()

    #Step 2. Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    texts = text_splitter.split_documents(documents)

    #Step 3. Store
    #convert text to embeddings
    embeddings=GooglePalmEmbeddings(google_api_key = api_key)
        
    # Supplying a persist_directory will store the embeddings on disk
    persist_directory = 'db'
    db = Chroma.from_documents(documents=texts,embedding=embeddings,persist_directory=persist_directory)
    
    print('Data load complete!')

def add_doc():
    vectorstore=read_data()

    loader = CSVLoader(file_path=r"C:\Users\leo.zhu\OneDrive - CBRE, Inc\Documents\Python AI Projects\TM1 Q&A2.csv")
    documents = loader.load()
    #Step 2. Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    texts = text_splitter.split_documents(documents)

    # Load and embed new documents
    vectorstore.add_documents(texts)
    # Persist the changes
    vectorstore.persist()
    print('Data add complete!')    

def read_data():
    embeddings=GooglePalmEmbeddings(google_api_key = api_key)
    persist_directory = 'TM1 AI Assistant Project/palm_db'#'C:/Users/Leo/OneDrive - CBRE, Inc/Documents/Python AI Projects/TM1 AI Assistant Project/palm_db'
    store = Chroma(persist_directory=persist_directory, 
                  embedding_function=embeddings)
    return store

def gen_answer(question):
    prompt_template = """As a TM1 system administrator, you will be presented with common questions and related answers about TM1. Your task is to provide the most effective response to the user based on established best practices.

    Here are the questions and related best practices for responding:
    {context}

    Question from the TM1 user:  
    {question}

    Please provide the most suitable response to be sent to the user. If the recommended response is irrelevant, please make it clear that the answer is from Google PaLM own knowledge.
    Always say "Happy querying! 😊" at the end of the answer.
    """
    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)

    db=read_data()
    llm = GooglePalm(google_api_key = api_key)
    llm.temperature = 0
    
    retriever=db.as_retriever(search_kwargs={"k": 1})

    qa_chain = RetrievalQA.from_chain_type(llm,
                                           chain_type="stuff",
                                           retriever=retriever,
                                           return_source_documents=True,
                                           chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    # answer=qa_chain.run(question)
    answer=qa_chain(question)
    return answer

st.set_page_config(page_title="TM1 AI Assistant", page_icon= ":ice_cube:")
if st.sidebar.button('Add Docs'):
    add_doc()
    
c1,c2=st.columns([4,1])
with c1:
    st.subheader("TM1 AI Assistant :hugging_face:")
# with c2:
#     img=Image.open(r'D:\LZhu Documents\Python Program\cbre.png')   
#     img=st.image(img)

# Chat History List
#Intialization key='msg'
if 'msg' not in st.session_state:
    st.session_state['msg']=[]

#to present historical chat msg
for msg in st.session_state['msg']:
    if isinstance(msg,dict):
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
            
# message = st.text_area("Question")
prompt=st.chat_input("Ask me anything about TM1...")
# if st.button('Answer'):
if prompt:
    #add data to session_state
    st.session_state['msg'].append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    with st.chat_message('assistant'):
        st.write("Generating best practice message...")
        result = gen_answer(prompt)
        st.session_state['msg'].append({'role': 'assistant', 'content': result.get('result')})
        st.info(result.get('result')) 
    
        st.divider()
        page_content_value = result['source_documents'][0].page_content
        st.caption('Source Documents :books:')
        st.markdown(page_content_value)

# streamlit run "C:\Users\Leo\OneDrive - CBRE, Inc\Documents\Python AI Projects\PostgreSQL DB\TM1 AI Assistant Project\tm1_ai_palm.py"
 # streamlit run "TM1 AI Assistant Project\pages\tm1_ai_PaLM.py"       