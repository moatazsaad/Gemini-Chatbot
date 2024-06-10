from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure genai library with the API key from the environment variable
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

    # Main application
    st.title("Gemini LLM Application")
    st.write("Welcome to Gemini LLM Application! Type your question below and click 'Ask the question' to get a response from Gemini AI.")

    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Input field for the user to ask questions
    input_text = st.text_input("Your Question:", key="input")

    # Button to submit the question
    submit = st.button("Ask the question")

    # Check if the submit button is clicked and input is provided
    if submit and input_text:
        # Get response from Gemini AI
        response = get_gemini_response(input_text)
        
        # Add user query and response to session chat history
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader("The Response is")
        
        # Display the response
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
    
    # Check if there's chat history to display
    if st.session_state['chat_history']:
        st.subheader("Chat History")
        # Display chat history
        for role, text in st.session_state['chat_history']:
            st.write(f"{role}: {text}")
