import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import load_documents, save_db, load_embeddings, load_db
import yaml
import fitz

# Hàm load cấu hình từ tệp config.yaml
def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config

# Load FAISS database
db = load_db(embedding_function=load_embeddings())

# Hàm xử lý PDF và chuyển thành vector
def process_pdf(pdf_path):
    # Load embeddings model
    embedding_function = load_embeddings()

    # Load PDF document
    pdf_documents = load_documents(pdf_path)

    # Extract text content from PDF
    pdf_text = ""
    for doc in pdf_documents:
        pdf_text += doc.text + "\n"

    # Convert text content to vector representation
    pdf_vector = embedding_function(pdf_text)

    return pdf_vector

# Load configuration
config = load_config()

# Load embeddings model
embedding_function = load_embeddings(
    model_name=config["embeddings"]["name"],
    model_kwargs={'device': config["embeddings"]["device"]}
)

# Load documents and create FAISS index
documents = load_documents("data/")
db = FAISS.from_documents(documents, embedding_function)
save_db(db)

# Tạo tiêu đề cho ứng dụng
st.sidebar.title("Ứng dụng Chatbot PDF")

# Widget để tải lên PDF
pdf_file = st.file_uploader("Tải lên PDF", type=["pdf"])

# Xử lý PDF được tải lên và thêm vào cơ sở dữ liệu
if pdf_file:
    with open("temp.pdf", "wb") as temp_pdf:
        temp_pdf.write(pdf_file.read())

    # Xử lý PDF và lấy biểu diễn vector của nó
    db = load_db(embedding_function=load_embeddings())
    db.add_documents(load_documents("/langchain_faiss_vectorindex"))
    save_db(db)

# Khởi tạo lịch sử trò chuyện
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Lấy đầu vào từ người dùng
user_input = st.text_input("Nhập câu hỏi của bạn:")

# Xử lý đầu vào của người dùng và hiển thị lịch sử trò chuyện
if user_input:
    # Truy vấn cơ sở dữ liệu để lấy câu trả lời
    similar_documents = db.similarity_search(user_input)

    # Tạo câu trả lời từ tài liệu liên quan nhất
    response = "Đây là kết quả mà tôi tìm thấy:\n"
    response += similar_documents[0].text  # Giả sử 'text' chứa nội dung của tài liệu

    # Thêm đầu vào của người dùng và câu trả lời vào lịch sử trò chuyện
    st.session_state.chat_history.append({"user": user_input, "bot": response})

    # Hiển thị lịch sử trò chuyện
    for entry in st.session_state.chat_history:
        st.text(f"Bạn: {entry['user']}")
        st.text(f"Bot: {entry['bot']}")
