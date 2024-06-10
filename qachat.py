from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import google.generativeai as genai

# Get the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=api_key)

    # Initialize the model and chat
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    # Function to get responses from the model
    def get_gemini_response(question):
        response = chat.send_message(question, stream=True)
        return response

    st.header("Gemini LLM Application")

    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    input_text = st.text_input("Input:", key="input")
    submit = st.button("Ask the question")

    if submit and input_text:
        response = get_gemini_response(input_text)
        # Add user query and response to session chat history
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
    
    st.subheader("The Chat History is")

    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
