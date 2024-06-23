import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import re
from flask import Flask, jsonify
from threading import Thread

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

    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(pdf_path):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    pdf_index_dir = os.path.join(INDEX_BASE_DIR, os.path.splitext(os.path.basename(pdf_path))[0])
    new_db = FAISS.load_local(pdf_index_dir, embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search("What is the document about?")

    chain = get_conversational_chain()
    response = chain({"input_documents": docs}, return_only_outputs=True)

    return response["output_text"]

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

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000, host='0.0.0.0')

