import streamlit as st
import os
import re
import openai

from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import RetrievalQA
os.environ["OPENAI_API_KEY"] = st.secrets["API"]


st.set_page_config(page_title="CHECK DETAILS FROM YOUR RESUME")
st.header("KNOW ABOUT APOSBOOK")


# upload file
pdf = "sodapdf-converted-2.pdf"
    
    # extract the text
if pdf is not None:
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        
      # split into chunks
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
    )
chunks = text_splitter.split_text(text)

embeddings = OpenAIEmbeddings()
knowledge_base = FAISS.from_texts(chunks, embeddings)



      

user_question = st.text_input("What do you want to know about AposBook")
if user_question:
    docs = knowledge_base.similarity_search(user_question)
            
    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type="stuff")
            

    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=user_question)
        print(cb)
              
     st.write(response)

