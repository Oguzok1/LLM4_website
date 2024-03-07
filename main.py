import streamlit as st
import time
from openai import OpenAI

st.title("Math Chat")

# Initialize the chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def response_generator(prompt: str, chat_history: list) -> None:
    client = OpenAI(api_key="sk-ccf6fdec8df54d9d8943c2f50dbfa8d4", base_url="https://api.deepseek.com/v1")

    # Append the user's prompt to the chat history
    chat_history.append({"role": "user", "content": prompt})

    unfiltered_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=chat_history
    )

    response = unfiltered_response.choices[0].message.content
    # Append the assistant's response to the chat history
    chat_history.append({"role": "assistant", "content": response})

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(response)

    print(chat_history)

# Display the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display the response
    with st.spinner("Thinking..."):
        response_generator(prompt, st.session_state.chat_history)
