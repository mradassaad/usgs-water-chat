"""
# My first app
Here's our first attempt at using data to create a table:
"""

import numpy as np
import pandas as pd
import streamlit as st
from langchain.llms import OpenAI

st.title("Chatbots for USGS knowledge base Q&A using OpenAI ChatGPT-3.5")

with st.sidebar:
    "## Chatbot Configuration"
    openai_api_key = st.text_input("**OpenAI API Key**", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    chatbot_type = st.radio("**Select Chatbot**", ["Knowledge Base Q&A", "Agent"])


def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(llm(input_text))


with st.form("my_form"):
    text = st.text_area(
        "Enter text:", "What are 3 key advice for learning how to code?"
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)
