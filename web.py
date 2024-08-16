import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import docx

import openai

load_dotenv()

openai.api_key = os.getenv("openai_api_key")
openai.api_base = os.getenv("openai_api_base")
openai.api_version = os.getenv("openai_api_version")
openai.api_type = os.getenv("openai_api_type")

def main():
    st.set_page_config(page_title="Docx Bot")
    st.header("Docx Bot")
    
    file = st.file_uploader("Upload docx",type=["docx","pdf"])
    if "submitted" not in st.session_state:
        st.session_state.submitted = False  

    if file is not None:
        if("pdf" in file.type):
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            doc = docx.Document(file)
            text = ""
            for para in doc.paragraphs:
                text += para.text
        
        chat_splitter = CharacterTextSplitter(separator="\n",chunk_size=1000,chunk_overlap=200,length_function=len)
        chunks = chat_splitter.split_text(text)

        def submit_text():
            st.session_state.submitted = True  
            st.session_state.saved_chat = st.session_state.input_text  
            st.session_state.input_text = "" 

        query = st.text_input("Enter question :",key='input_text',on_change=submit_text)
        if st.session_state.submitted and st.session_state.saved_chat: 
            response = openai.ChatCompletion.create(engine="gpt-35-turbo", messages=[
                {"role":"system","content":f"You need to answer according to this file only , don't copy exact information :- {chunks}"},
                {"role":"user","content":st.session_state.saved_chat},
            ], stream=False, temperature=0.4, top_p=1)
            st.write(response.choices[0].message.content)

if(__name__ == '__main__'):
    main()