from langchain.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from utils import load_documents, save_db

# Khởi tạo mô hình nhúng
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L6-v2")

# Nhúng tài liệu
documents = load_documents("data/")
# Sử dụng phương thức encode
embedded_docs = [embedding_model.encode(doc) for doc in documents]

# Tạo và lưu chỉ mục FAISS
db = FAISS.from_documents(documents, embedded_docs)
print("Index Created")
save_db(db)
