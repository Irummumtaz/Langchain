import requests
import streamlit as st

def get_openai_response(input_text):
    response=requests.post('https:/localhost:8000/essays/invoke')
    json={'input':{'topic':input_text}}

    return response.json()['output']['content']


def get_ollama_response(input_text):
    response=requests.post('https:/localhost:8000/poem/invoke')
    json={'input':{'topic':input_text}}

    return response.json()['output']['content']


#streamlit

st.title('Langchain Demo')
input_text=st.text_input('Write an Essay')
input_text1=st.text_input('Write a Poem')

if input_text:
    st.write(get_openai_response(input_text))

if input_text1:
    st.write(get_ollama_response(input_text1))