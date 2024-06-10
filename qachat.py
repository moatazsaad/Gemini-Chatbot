from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configures genai library with the API key from the environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load OpenAI model and get responses
def get_gemini_response(input, image):
    model = None
    if image:
        model = genai.GenerativeModel('gemini-pro-vision')
    else:
        model = genai.GenerativeModel('gemini-pro')
    
    if model:
        if image and input:
            # Generate content using both input and image
            response = model.generate_content([input, image])
        elif input:
            response = model.generate_content(input)
        else:
            return "Please provide a question or upload an image."
        
        return response.text
    else:
        return "Model loading failed. Please try again."

# Initialize our streamlit app
st.set_page_config(page_title="Gemini AI Image and Text Analyzer")

st.title("Gemini AI Image and Text Analyzer")
st.write("Upload an image or provide a text prompt to get a response from the Gemini AI.")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Creates a text input field for the user
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Initializes the image variable as an empty string
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # Display the uploaded image.
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Analyze")

# Checks if the submit button is clicked
if submit:
    if not input_text and not uploaded_file:
        st.error("Please provide a question or upload an image.")
    else:
        with st.spinner("Processing..."):
            response = get_gemini_response(input_text, image)
        st.subheader("The Response is")
        st.write(response)
        
        # Add user query and response to session chat history
        if input_text:
            st.session_state['chat_history'].append(("You", input_text))
        st.session_state['chat_history'].append(("Bot", response))

# Display chat history only if there is any
if st.session_state['chat_history']:
    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

# Option to clear chat history
if st.button("Clear Chat History"):
    st.session_state['chat_history'] = []
    st.experimental_rerun()
