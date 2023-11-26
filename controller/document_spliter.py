from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
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

    def split_by_token(self, docs_file_loaded, chunk_size=500, chunk_overlap=25):

        text_splitter = TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap)
        self.documents = text_splitter.split_documents(docs_file_loaded)
        # print(len(self.documents))
        return self.documents
