import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Constants
INDEX_BASE_DIR = "indexes"


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
    I want you describe in brief what the company has in their document, you should maintain the sentiment they have. Keep in mind that you are mainly focused on Health, Water and Sanitation related concepts. Limit it to 100 words only! \n\n
    Context:\n {context}\n
    Question: \n{question}\n
    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question, pdf_name):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    pdf_index_dir = os.path.join(INDEX_BASE_DIR, pdf_name)
    new_db = FAISS.load_local(pdf_index_dir, embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

    print(response)
    st.write("Reply: ", response["output_text"])


def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with PDF using Gemini💁")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        # Extract the PDF name from the user question (assuming it's included)
        pdf_name = st.selectbox("Select PDF", os.listdir(INDEX_BASE_DIR))
        if pdf_name:
            user_input(user_question, pdf_name)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                for pdf in pdf_docs:
                    raw_text = get_pdf_text([pdf])
                    text_chunks = get_text_chunks(raw_text)
                    pdf_name = os.path.splitext(pdf.name)[0]  # Get PDF name without extension
                    get_vector_store(text_chunks, pdf_name)
                st.success("Done")


if __name__ == "__main__":
    main()
