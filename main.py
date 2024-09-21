import streamlit as st
from streamlit import session_state as ss
import os
# Import modules
from openai_backend import Assistant


api_key=st.secrets["openai_secret_key"]

# Initialize agent
if 'agent' not in ss:
    ss.agent = Assistant()
    ss.initial_message_shown = False
    ss.chat_history = []

# Streamlit app configuration
st.set_page_config(
    page_title="Course Roadmap",
    page_icon="🕮",
)

# App title
st.title("💡:blue[Course Roadmap] :red[Chatbot]")

# Display initial message if not shown before
if not ss.initial_message_shown:
    initial_message = "Hello! I'm your Course Roadmap Chatbot. How can I assist you today?"
    ss.initial_message_shown = True
    ss.chat_history.append({"role": "assistant", "content": initial_message})

# Display chat messages from history on app rerun
for message in ss.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter your text here!"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to app chat history
    ss.chat_history.append({"role": "user", "content": prompt})
    
    # Send message to chatbot
    ss.agent.add_user_prompt("user", prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Empty container to display the assistant's reply
        assistant_reply_box = st.empty()

        # Initialize the assistant reply as an empty string
        assistant_reply = ""

        # Stream the assistant's response
        assistant_reply = ss.agent.stream_response(assistant_reply_box)

        # Once the stream is over, update chat history
        ss.chat_history.append({"role": "assistant", "content": assistant_reply})
