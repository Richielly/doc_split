from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

class VectorStore:

    def save_faiss(self, docs):
        embeddings_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.from_documents(docs, embeddings_function)
        db.save_local("./vector_storage_house_faiss/geral")
        return db

    def get_faiss(self):
        embeddings_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        db_faiss = FAISS.load_local("./vector_storage_house_faiss/geral", embeddings_function)
        return db_faiss
