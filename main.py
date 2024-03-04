import streamlit as st 
import random
import time




# Streamlit app
st.title("Hello, Vlad\nHow can I assist you today?")

# Function to generate a response
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Get user input
prompt = st.chat_input("Send a message")

# If there's a prompt, add it to the messages and generate a response
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display the response
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())

# Print the current session state for debugging
print(st.session_state)
