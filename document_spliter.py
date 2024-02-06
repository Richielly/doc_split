from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
import re
class DocumentSpliter:
    def __init__(self):
        self.documents = []
    def split_by_word(self, docs_file_loaded, chunk_size=1000, chunk_overlap=25):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.documents = text_splitter.split_documents(docs_file_loaded)
        # print(len(self.documents))
        return self.documents

    def split_by_word_without_space(self, docs_file_loaded, chunk_size=1000, chunk_overlap=25):
        processed_docs = []
        for doc in docs_file_loaded:
            # Certifique-se de que 'doc' é uma string
            if isinstance(doc, str):
                # Pré-processamento para remover quebras de linha e espaços em branco consecutivos
                processed_text = re.sub(r'\n+', '\n', doc)  # Remove múltiplas quebras de linha
                processed_text = re.sub(r' +', ' ', processed_text)  # Remove espaços em branco consecutivos
                processed_docs.append(processed_text)
            else:
                # Adicione um tratamento de erro ou uma mensagem de log aqui se necessário
                pass

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.documents = text_splitter.split_documents(processed_docs)
        return self.documents

    def split_by_token(self, docs_file_loaded, chunk_size=500, chunk_overlap=25):

        text_splitter = TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap)
        self.documents = text_splitter.split_documents(docs_file_loaded)
        # print(len(self.documents))
        return self.documents
