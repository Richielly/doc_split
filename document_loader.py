import os
import re

from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader

import fitz  # Importa a biblioteca PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pdf2docx import Converter
from pikepdf import Pdf, PdfImage

class DocumentLoader:

    def listar_arquivos_pdf(self, entrada):
        """
        Esta função aceita um diretório, um caminho de arquivo único ou uma lista de caminhos de arquivos.
        Se for um diretório, ela lista todos os arquivos PDF nele e em suas subpastas.
        Se for um caminho de arquivo ou uma lista, ela verifica se os arquivos são PDF e os adiciona à lista.

        Args:
        entrada (str ou list): Um diretório, um caminho de arquivo único ou uma lista de caminhos de arquivos.

        Returns:
        list: Uma lista contendo os caminhos completos dos arquivos PDF encontrados ou especificados.
        """
        arquivos_pdf = []

        if isinstance(entrada, list):
            # Se a entrada for uma lista, verifica cada item para garantir que é um arquivo PDF.
            for item in entrada:
                if os.path.isfile(item) and item.lower().endswith('.pdf'):
                    arquivos_pdf.append(item)
        elif os.path.isdir(entrada):
            # Se a entrada for um diretório, busca todos os arquivos PDF nele.
            for raiz, diretorios, arquivos in os.walk(entrada):
                for arquivo in arquivos:
                    if arquivo.lower().endswith('.pdf'):
                        caminho_completo = os.path.join(raiz, arquivo)
                        arquivos_pdf.append(caminho_completo)
        elif os.path.isfile(entrada) and entrada.lower().endswith('.pdf'):
            # Se a entrada for um caminho de arquivo único e for um PDF.
            arquivos_pdf.append(entrada)

        return arquivos_pdf

    def get_files(self, files_path):
        pdf_files = []

        for file in os.listdir(files_path):
            if file.endswith('.pdf'):
                pdf_files.append(f'{files_path}/{file}')
        return pdf_files

    def load_pdf(self, pdf_files):
        def limpar_texto(texto):
            # texto_limpo = re.sub(r'[^\x20-\x7E\n]', '', texto)  # Remove caracteres não ASCII exceto quebras de linha
            texto_limpo = re.sub(r'\s\s+', ' ', texto).strip()  # Normaliza espaços
            return texto_limpo

        all_pages_content = ""
        for pdf_file in pdf_files:

            loader = PyPDFLoader(pdf_file, extract_images=False)
            pages = loader.load()
            for page in pages:
                all_pages_content += page.page_content + "\n"  # Adiciona uma quebra de linha entre o conteúdo das páginas
            # Aplica a limpeza ao texto consolidado
            all_pages_content = limpar_texto(all_pages_content)
            # Cria um único objeto Document com o conteúdo consolidado
            consolidated_document = Document(page_content=all_pages_content, metadata={'source': pdf_file, 'page': len(pages)})
            # full_pages.extend(pages)
            # print(f"Carregando arquivo: {pdf_file}")
        # print(len(pdf_files), len(full_pages))
        print([consolidated_document])
        return [consolidated_document]

    def filter_docs(self, docs_list, excluded_pages):
        return [doc for doc in docs_list if doc.metadata['page'] not in excluded_pages]

    def extrair_texto_pdf(self, caminho_pdf, paginas_a_ignorar="", image=False):
        """
        Extrai o texto de um arquivo PDF, removendo toda a formatação e permitindo a opção de ignorar páginas específicas.

        :param caminho_pdf: Caminho do arquivo PDF a ser lido.
        :param paginas_a_ignorar: String contendo os números das páginas a serem ignoradas, separadas por vírgulas.
        :return: String contendo o texto extraído.
        """

        # Converte a string de páginas em uma lista de inteiros, ajustando a indexação para começar em 0
        try:
            paginas_a_ignorar = [int(pagina) - 1 for pagina in paginas_a_ignorar.split(',') if pagina.isdigit()]
        except ValueError:
            raise ValueError("Erro ao converter páginas a ignorar para inteiros.")

        texto = ''

        # Usa o contexto de abertura do PyMuPDF
        try:
            with fitz.open(caminho_pdf) as documento:
                # Itera sobre cada página do documento
                for num_pagina, pagina in enumerate(documento):
                    # Verifica se a página atual é uma das páginas a serem ignoradas
                    if num_pagina in paginas_a_ignorar:
                        continue

                    # Extrai o texto da página e concatena com a string de texto
                    texto += pagina.get_text()

            # Extrair imagens
            if image:
                try:
                    arquivo = Pdf.open(caminho_pdf)
                    for pagina in arquivo.pages:
                        for nome, imagem in pagina.images.items():
                            imagem_salvar = PdfImage(imagem)
                            imagem_salvar.extract_to(fileprefix=f"imagens/{nome}")
                except Exception as e:
                    raise Exception(f"Erro ao extrair imagens: {e}")

            return texto.replace('\n', '').replace('.', '.\n')

        except Exception as e:
            raise Exception(f"Erro ao extrair texto do PDF: {e}")

    # Converter pdf em docx
    def convert_pdf_to_docx(self, caminho_pdf, pages=None):
        docx_file = caminho_pdf.split('.')[0] + '.docx'
        # convert pdf to docx
        cv = Converter(caminho_pdf)
        cv.convert(docx_file, pages=pages)  # todas as paginas por padrão
        cv.close()

    def texto_para_pdf(self, texto, caminho_saida):
        """
        Converte uma string de texto em um arquivo PDF, evitando sobreposição de texto.

        :param texto: String contendo o texto a ser convertido.
        :param caminho_saida: Caminho do arquivo PDF de saída.
        """
        c = canvas.Canvas(caminho_saida, pagesize=letter)
        largura_pagina, altura_pagina = letter

        # Configuração da margem e posição inicial
        margem = 40
        x = margem
        y = altura_pagina - margem

        # Configuração de fonte e tamanho
        tamanho_fonte = 10
        c.setFont("Helvetica", tamanho_fonte)
        altura_linha = 14

        for linha in texto.split('\n'):
            palavras = linha.split()
            linha_atual = ''
            for palavra in palavras:
                # Verifica se a linha excede a largura da página
                if c.stringWidth(linha_atual + ' ' + palavra, "Helvetica", tamanho_fonte) > (
                        largura_pagina - 2 * margem):
                    # Desenha a linha e reseta a linha_atual
                    c.drawString(x, y, linha_atual)
                    y -= altura_linha  # Move para a próxima linha
                    linha_atual = palavra  # Começa uma nova linha
                else:
                    # Adiciona a palavra na linha atual
                    linha_atual += f' {palavra}' if linha_atual else palavra

            # Desenha a última linha
            c.drawString(x, y, linha_atual)
            y -= altura_linha  # Move para a próxima linha

            # Verifica se precisa de uma nova página
            if y < margem:
                c.showPage()
                c.setFont("Helvetica", tamanho_fonte)
                y = altura_pagina - margem  # Reseta a posição Y para o topo da nova página

        c.save()
        return caminho_saida


 # def documents_tranforme(self, documents_list):
    #     documents = []
    #     for result in documents_list:
    #         # documents.append(Document(
    #         #     page_content=result.summary,
    #         #     metadata={"source": result.entry_id},
    #         # ))
    #     return documents




########Versão antiga funcionando#############################################################################################################
# import os
# from langchain.docstore.document import Document
# from langchain.document_loaders import PyPDFLoader
# import re
# class DocumentLoader:

#     def get_files(self, files_path):
#         pdf_files = []

#         for file in os.listdir(files_path):
#             if file.endswith('.pdf'):
#                 pdf_files.append(f'{files_path}/{file}')
#         return pdf_files

#     #Separando documento por pagina
#     # def load_pdf(self, pdf_file):
#     #     full_pages = []
#     #     loader = PyPDFLoader(pdf_file, extract_images=False)
#     #     pages = loader.load()
#     #
#     #     full_pages.extend(pages)
#     #     return full_pages

#     #Unindo todas as paginas em um documento
#     def load_pdf(self, pdf_file):
#         # Inicializa a string que vai conter o conteúdo consolidado de todas as páginas
#         all_pages_content = ""

#         # Supondo que PyPDFLoader e a função load() já estejam definidos corretamente
#         loader = PyPDFLoader(pdf_file, extract_images=False)
#         pages = loader.load()

#         # Concatena o conteúdo de todas as páginas
#         for page in pages:
#             all_pages_content += page.page_content + "\n"  # Adiciona uma quebra de linha entre o conteúdo das páginas

#         # Cria um único objeto Document com o conteúdo consolidado e algum metadado exemplificativo
#         consolidated_document = Document(page_content=all_pages_content,
#                                          metadata={'source': pdf_file, 'page': len(pages)})

#         # Retorna uma lista contendo apenas o objeto Document consolidado
#         print([consolidated_document])
#         return [consolidated_document]

#     def filter_docs(self, docs_list, excluded_pages):
#         excluded_pages = [int(x) - 1 for x in excluded_pages]
#         return [doc for doc in docs_list if doc.metadata['page'] not in excluded_pages]

#     def remove_extra_newlines(self, text):
#         # Substitui três ou mais \n seguidos por apenas dois \n
#         return re.sub(r'\n{3,}', '\n\n', text)

#     def remove_crlf(self, text):
#         # Substitui todas as ocorrências de \r\n por uma string vazia
#         return text.replace('\r\n', '##')

#     def preprocessar_texto(self, texto):
#         # Removendo caracteres especiais e múltiplos espaços
#         texto = re.sub(r'\s{3,}', '\n', texto)
#         return texto

#     def remover_repeticoes_globais(self, textos, trecho):
#         """
#         Remove as repetições de um trecho em uma lista de textos, mantendo apenas a primeira ocorrência global.
#         """
#         texto_completo = ''.join(textos)  # Concatena todos os textos em um único texto
#         primeira_ocorrencia = True

#         def substituir_trecho(match):
#             nonlocal primeira_ocorrencia
#             if primeira_ocorrencia:
#                 primeira_ocorrencia = False
#                 return match.group(0)  # Mantém a primeira ocorrência
#             return ''  # Remove as repetições subsequentes

#         texto_atualizado = re.sub(re.escape(trecho), substituir_trecho, texto_completo)
#         return texto_atualizado

#     # def documents_tranforme(self, documents_list):
#     #     documents = []
#     #     for result in documents_list:
#     #         # documents.append(Document(
#     #         #     page_content=result.summary,
#     #         #     metadata={"source": result.entry_id},
#     #         # ))
#     #     return documents



    ###############################################################################################################