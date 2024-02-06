import os
# from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader
import re
class DocumentLoader:

    def get_files(self, files_path):
        pdf_files = []

        for file in os.listdir(files_path):
            if file.endswith('.pdf'):
                pdf_files.append(f'{files_path}/{file}')
        return pdf_files

    # def load_pdf(self, pdf_files):
    #     print(list(pdf_files))
    #     full_pages=[]
    #     pages = []
    #     for pdf_file in pdf_files:
    #         loader = PyPDFLoader(pdf_file)
    #         pages = loader.load()
    #         full_pages.extend(pages)
    #         # print(f"Carregando arquivo: {pdf_file}")
    #     # print(len(pdf_files), len(full_pages))
    #
    #     return full_pages

    def load_pdf(self, pdf_file):
        full_pages = []
        loader = PyPDFLoader(pdf_file)
        pages = loader.load()
        full_pages.extend(pages)
        # for page in pages:
        #     # Remove quebras de linha da página atual e adiciona à lista full_pages
        #     full_pages.append(page.replace('\n', ''))
            # print(f"Carregando arquivo: {pdf_file}")
        # print(len(pdf_files), len(full_pages))

        return full_pages

    def filter_docs(self, docs_list, excluded_pages):
        excluded_pages = [int(x) - 1 for x in excluded_pages]
        return [doc for doc in docs_list if doc.metadata['page'] not in excluded_pages]

    def remove_extra_newlines(self, text):
        # Substitui três ou mais \n seguidos por apenas dois \n
        return re.sub(r'\n{3,}', '\n\n', text)

    def remove_crlf(self, text):
        # Substitui todas as ocorrências de \r\n por uma string vazia
        return text.replace('\r\n', '##')


    # def documents_tranforme(self, documents_list):
    #     documents = []
    #     for result in documents_list:
    #         # documents.append(Document(
    #         #     page_content=result.summary,
    #         #     metadata={"source": result.entry_id},
    #         # ))
    #     return documents