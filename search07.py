import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import re
from flask import Flask, jsonify
from threading import Thread
import requests
import json
from groq import Groq

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

# Constants
INDEX_BASE_DIR = "indexes"
DOWNLOADS_FOLDER = "downloads"

# Global dictionary to store responses
pdf_responses = {}

# Function to sanitize filenames
def sanitize_filename(filename):
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks, pdf_name):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)

    # Create a directory for the FAISS index if it doesn't exist
    pdf_index_dir = os.path.join(INDEX_BASE_DIR, pdf_name)
    os.makedirs(pdf_index_dir, exist_ok=True)

    # Save the FAISS index in the directory
    vector_store.save_local(pdf_index_dir)

def get_conversational_chain():
    prompt_template = """
    You are a highly advanced language model with extensive knowledge and exceptional comprehension skills. You have been provided with text extracted from a company's PDF document. Your task is to analyze the text and provide a comprehensive and accurate summary focusing on Water, Sanitation, and Hygiene (WASH). Ensure to include any numbers or statistics mentioned in these domains. The summary should be around 200 words and formatted as JSON.\n\n
    {context}\n
    Question: \nWhat is the document about?\n
    Answer: A brief overall summary of the company's efforts in Water, Sanitation, and Hygiene, including key numbers and achievements that are related to WASH.
    
    """

    return prompt_template

def user_input(pdf_path):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    pdf_index_dir = os.path.join(INDEX_BASE_DIR, os.path.splitext(os.path.basename(pdf_path))[0])
    # Assuming FAISS loading and similarity search here as before

    # Groq API configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Replace with your API key

    # Fetch the conversational response from Groq
    client = Groq(api_key=GROQ_API_KEY)

    prompt = get_conversational_chain()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": f"PDF: {pdf_path}",  # Provide additional context or metadata
            },
        ],
        model="llama3-8b-8192",
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    message_content = chat_completion.choices[0].message.content

    return message_content

def process_pdf(pdf_path):
    raw_text = get_pdf_text([pdf_path])
    text_chunks = get_text_chunks(raw_text)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Get PDF name without extension
    get_vector_store(text_chunks, pdf_name)
    return pdf_name

# Function to get the path to the Downloads folder within the base project folder
def get_downloads_folder():
    return os.path.join(os.path.dirname(__file__), DOWNLOADS_FOLDER)

# Function to process PDF asynchronously
def process_pdf_async(pdf_file):
    try:
        pdf_name = process_pdf(pdf_file)
        answer = user_input(pdf_file)
        pdf_responses[pdf_name] = {"response": answer}
    except Exception as e:
        pdf_responses[pdf_file] = {"error": str(e)}

# Route to process all PDFs in the Downloads folder
@app.route('/process_all_pdfs', methods=['GET'])
def process_all_pdfs():
    global pdf_responses
    downloads_folder = get_downloads_folder()
    pdf_files = [os.path.join(downloads_folder, file) for file in os.listdir(downloads_folder) if file.lower().endswith('.pdf')]

    if not pdf_files:
        return jsonify({"error": "No PDF files found in the Downloads folder."}), 404

    # Clear previous responses
    pdf_responses = {}

    # Process each PDF file asynchronously
    threads = []
    for pdf_file in pdf_files:
        thread = Thread(target=process_pdf_async, args=(pdf_file,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return jsonify(pdf_responses), 200

@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    try:
        response = requests.get('http://localhost:5000/process_all_pdfs')
        data = response.json()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000, host='0.0.0.0')
