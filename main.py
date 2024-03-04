import streamlit as st
import random
import time
from tinydb import TinyDB
import requests
import json

# Function to load or create chat history
def load_chat_history():
    filename = "all_chat_history.json"
    db = TinyDB(filename)
    return db

# Initialize or load chat history
db = load_chat_history()

ask_for_password = st.title("Please enter your username and password")

# Placeholder for user name input
name_placeholder = st.empty()
# Get user identifier (for example, username)
user_id = name_placeholder.text_input("Enter your name:")

# Proceed if the user provided a name
if user_id:
    ask_for_password.empty()
    st.title(f"Hello, {user_id}!\nHow can I assist you today?")

    # Initialize chat history from previous sessions
    chat_history = db.all()

    # Display chat messages from history on app rerun
    for message in chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input if assistant is not responding
    prompt = st.chat_input("Type something...")

    if prompt:
        # Add user message to chat history
        user_message = {"role": "user", "content": prompt}
        chat_history.append(user_message)
        db.insert(user_message)

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Simulate assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            url = "https://api.deepseek.com/v1/chat/completions"

            payload = json.dumps({
                "messages": [
                    {
                        "content": "You are a helpful assistant",
                        "role": "system"
                    },
                    {
                        "content": user_message['content'],
                        "role": "user"
                    }
                ],
                "model": "deepseek-coder",
                "frequency_penalty": 0,
                "max_tokens": 2048,
                "presence_penalty": 0,
                "stop": None,
                "stream": False,
                "temperature": 1,
                "top_p": 1
            })
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer sk-ccf6fdec8df54d9d8943c2f50dbfa8d4'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            assistant_response = response.json().get('choices')[0]['message']['content']

            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            assistant_message = {"role": "assistant", "content": full_response}
            chat_history.append(assistant_message)
            db.insert(assistant_message)

    # Hide the user name input after it's provided
    name_placeholder.empty()
