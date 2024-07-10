# streamlit-chat-gpt.py
import streamlit as st
import langchain
langchain.debug = True
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

from models.models import load_gpt3_5, load_gpt4

llm = load_gpt4()

prompt = ChatPromptTemplate.from_template(
  # "Please answer the following question as briefly as possible: {question}"
  "Please answer the following question: {question}"
)
chain = prompt | llm | StrOutputParser()

st.title("ESRE Engineer ChatGPT Client")
question = st.chat_input("Enter your question ")
if question:
  st.chat_message("user").markdown(question)
  answer = chain.invoke({"question": question})
  st.chat_message("assistant").markdown(answer)
