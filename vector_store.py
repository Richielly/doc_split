import os

from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

class VectorStore:

    def save_faiss(self, docs, vetor_name):
        embeddings_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.from_documents(docs, embeddings_function)
        db.save_local(f"./vector_storage_house_faiss/{vetor_name}")
        return db

    def get_faiss(self, vetor_name):
        embeddings_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        db_faiss = FAISS.load_local(f"./vector_storage_house_faiss/{vetor_name}", embeddings_function, allow_dangerous_deserialization=True)
        return db_faiss

    def get_list_faiss(self, diretorio="./vector_storage_house_faiss/"):
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        itens = os.listdir(diretorio)
        # Filtra apenas os que são diretórios
        pastas = [item for item in itens if os.path.isdir(os.path.join(diretorio, item))]
        return pastas
