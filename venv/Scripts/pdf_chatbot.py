import streamlit as st
import fitz  
import requests

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variable
openai_api_key = os.environ.get('openai_api_key')
openai_endpoint = "https://api.openai.com/v1/completions"

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to chat with OpenAI
def chat_with_openai(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "prompt": prompt,
        "model": "davinci",
        "temperature": 0.7,
        "max_tokens": 150
    }
    response = requests.post(openai_endpoint, json=data, headers=headers)
    response_data = response.json()
    choices = response_data.get("choices", [])
    if choices:
        return choices[0]["text"].strip()
    else:
        return "Error: Unable to generate a response from the AI model."

# Streamlit app
def main():
    st.title("PDF Chatbot")
    st.write("Upload a PDF file and start chatting with its contents!")

    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        st.write("PDF Contents:")
        st.write(text)

        st.write("Chat with PDF contents:")
        user_input = st.text_input("You:", "")
        if st.button("Send"):
            conversation = f"You: {user_input}\nBot:"
            bot_response = chat_with_openai(conversation)
            st.write(bot_response)

if __name__ == "__main__":
    main()
