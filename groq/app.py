import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import OllamaEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS

import time
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv


load_dotenv()
#Load groq API

groq_api_key=os.getenv('GROQ_API_KEY')
 
if 'vectors' not in st.session_state:
    st.session_state.embeddings = OllamaEmbeddings(model="llama2")
    st.session_state.loader=WebBaseLoader('https://python.langchain.com/docs/introduction/')
    st.session_state.docs=st.session_state.loader.load()

    st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

    st.session_state.final_document=st.session_state.text_splitter.split_documents( st.session_state.docs[:50])

    st.session_state.vectors=FAISS.from_documents( st.session_state.final_document,st.session_state.embeddings)

st.title('Chat Groq')s
llm=ChatGroq(groq_api_key=groq_api_key,
             model_name='llama-3.3')

prompt=ChatPromptTemplate.from_template(
    '''
Answer the question based on provided context only.
Please provide the most accurate response based on the question.
<context>
{context}
</context>
Questions:{input}
    '''
)

document_chain=create_stuff_documents_chain(llm,prompt)
retriever=st.session_state.vectors.as_retriver()
retriever_chain=create_retrieval_chain(retriever,document_chain)

prompt=st.text_input('Input Your Prompt here')
if prompt:
    start=time.process_time()
    response=retriever_chain.invoke({'input':prompt})
    print('Response time:',time.process_time()-start)        

    st.write(response['answer'])

    with st.expander('Documents Similaity Search'):
        #find the relevant chunk
        for i,doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write('-----------------------------')