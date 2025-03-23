import streamlit as st
import subprocess
import socket
import time
import sys
import requests 
import ast


# ✅ Always call this first in Streamlit
st.set_page_config(page_title="Chat with AI", layout="centered")


# ✅ Title after set_page_config (only once at the top!)
st.title("💬 News Summarization application Created BY Krishna Runwal")



# ✅ Clear Chat Button
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Type your message here...")

if user_input:
    
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ✅ Spinner while thinking
    with st.spinner("I am scrapping Articles for you... 🤔"):
        # 🔗 Call your API
        try:
            res = requests.post("http://localhost:5000/get-summaries_of_article", json={"user_input": user_input})
            print("🔍 Raw response:", res.text)
    
            if res.status_code != 200:
                raise Exception(f"Status code: {res.status_code} | Error: {res.text}")
    
            response_data = res.json()
            if "response" not in response_data:
                raise Exception("Missing 'response' key in API response")
    
            response = ast.literal_eval(response_data["response"])
            
    

        except Exception as e:
            response = {"error": f"❌ API Error: {str(e)}"}
            hindi_content = None

    # ✅ Handle dict response nicely
    with st.chat_message("assistant"):
        if isinstance(response, dict):
            st.json(response)
        else:
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})