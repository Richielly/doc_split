import os
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader
import re
class DocumentLoader:

    def get_files(self, files_path):
        pdf_files = []

        for file in os.listdir(files_path):
            if file.endswith('.pdf'):
                pdf_files.append(f'{files_path}/{file}')
        return pdf_files

    #Separando documento por pagina
    # def load_pdf(self, pdf_file):
    #     full_pages = []
    #     loader = PyPDFLoader(pdf_file, extract_images=False)
    #     pages = loader.load()
    #
    #     full_pages.extend(pages)
    #     return full_pages

    #Unindo todas as paginas em um documento
    def load_pdf(self, pdf_file):
        # Inicializa a string que vai conter o conteúdo consolidado de todas as páginas
        all_pages_content = ""

        # Supondo que PyPDFLoader e a função load() já estejam definidos corretamente
        loader = PyPDFLoader(pdf_file, extract_images=False)
        pages = loader.load()

        # Concatena o conteúdo de todas as páginas
        for page in pages:
            all_pages_content += page.page_content + "\n"  # Adiciona uma quebra de linha entre o conteúdo das páginas

        # Cria um único objeto Document com o conteúdo consolidado e algum metadado exemplificativo
        consolidated_document = Document(page_content=all_pages_content,
                                         metadata={'source': pdf_file, 'page': len(pages)})

        # Retorna uma lista contendo apenas o objeto Document consolidado
        print([consolidated_document])
        return [consolidated_document]

    def filter_docs(self, docs_list, excluded_pages):
        excluded_pages = [int(x) - 1 for x in excluded_pages]
        return [doc for doc in docs_list if doc.metadata['page'] not in excluded_pages]

    def remove_extra_newlines(self, text):
        # Substitui três ou mais \n seguidos por apenas dois \n
        return re.sub(r'\n{3,}', '\n\n', text)

    def remove_crlf(self, text):
        # Substitui todas as ocorrências de \r\n por uma string vazia
        return text.replace('\r\n', '##')

    def preprocessar_texto(self, texto):
        # Removendo caracteres especiais e múltiplos espaços
        texto = re.sub(r'\s{3,}', '\n', texto)
        return texto

    def remover_repeticoes_globais(self, textos, trecho):
        """
        Remove as repetições de um trecho em uma lista de textos, mantendo apenas a primeira ocorrência global.
        """
        texto_completo = ''.join(textos)  # Concatena todos os textos em um único texto
        primeira_ocorrencia = True

        def substituir_trecho(match):
            nonlocal primeira_ocorrencia
            if primeira_ocorrencia:
                primeira_ocorrencia = False
                return match.group(0)  # Mantém a primeira ocorrência
            return ''  # Remove as repetições subsequentes

        texto_atualizado = re.sub(re.escape(trecho), substituir_trecho, texto_completo)
        return texto_atualizado

    # def documents_tranforme(self, documents_list):
    #     documents = []
    #     for result in documents_list:
    #         # documents.append(Document(
    #         #     page_content=result.summary,
    #         #     metadata={"source": result.entry_id},
    #         # ))
    #     return documents