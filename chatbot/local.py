from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


os.environ['LANGCHAIN_TRACING-V2']='True'
os.environ['LANGCHAIN_API_KEY']=os.getenv('LANGCHAIN_API_KEY')

#Prompt Template
Prompt=ChatPromptTemplate.from_messages(
    [
        ('system','You are helpful assistant, please response to the user queries')
        ('user','Question:{question}')
    ]

)

##Streamlit Framework

st.title('Langchain Chatbot Demo')
input_text=st.input_text('Search the Topic you want ')


#Ollama LLM

llm=Ollama(model='llama2')
output_parser=StrOutputParser()
chain=Prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))

