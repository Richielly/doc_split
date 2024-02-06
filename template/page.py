import os
import time

import flet as ft
import document_loader
import document_spliter
import tik_token
import vector_store
import ia_retriever
import sys
import os

def pages(page: ft.Page):


    if getattr(sys, 'frozen', False):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.abspath(".")

    path_to_file = os.path.join(basedir, 'langchain', 'chains', 'llm_summarization_checker', 'prompts','create_facts.txt')

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_center()
    page.title = "Gerenciador de arquivos IA" + " V_2.0.0"
    page.icon = "imagem_principal.png"
    progressBar = ft.ProgressBar(width=1000, color=ft.colors.DEEP_ORANGE, value=0)
    progressBar_chunk = ft.ProgressBar(width=1000, color=ft.colors.BROWN_500, visible=False)

    def pick_files_result(e: ft.FilePickerResultEvent):

        selected_files.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelado!"
        )
        selected_files.update()
        if selected_files.value and selected_files.value != 'Cancelado!':
            btn_processar.visible = True
            btn_processar.disabled = False
            page.update()
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    page.overlay.append(pick_files_dialog)

    btn_procurar_arquivo = (
        ft.Row(
            [
                ft.ElevatedButton(
                    "Arquivo",
                    width=200,
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False,
                        initial_directory=os.getcwd()
                    ),
                ),
                selected_files,
            ]
        )
    )

    def btn_processar(e):
        btn_processar.disabled=True
        page.update()
        text = ""
        doc_inf = True
        doc = document_loader.DocumentLoader()
        tokens = tik_token.TikToken()
        total_tokens=0
        paginas = 0

        if pagina.value:
            documentos = doc.filter_docs(doc.load_pdf(selected_files.value), pagina.value.split(','))
        else:
            documentos = doc.load_pdf(selected_files.value)

        for pag in documentos:
            time.sleep(0.2)
            paginas+=1
            progressBar.value = 100/len(documentos)/100 * paginas
            progressBar.update()
            page.update()
            num_tokens = tokens.num_tokens_from_string(pag.page_content)
            total_tokens+=num_tokens
            rest = doc.remove_crlf(pag.page_content)
            if doc_inf:
                text = text+'\n'+'-'*90 + ' → pagina ' +str(pag.metadata['page']+1) +'-'*90 +f'\n🪙 tokens:  {num_tokens}\n'+rest

        tokens_total.value = f'💰 {total_tokens} tokens total.\n 💵 '+ str((total_tokens / 1000) * 0.001) + ' custo.'
        paginas_total.value = f'📃 {paginas}'
        container_1.content=ft.Text(text, selectable=True)
        page.window_maximized = False
        btn_gerar_split.visible = True
        btn_gerar_split.disabled = False
        t.selected_index=1
        progressBar.value = 0
        page.update()

    def btn_chunk(e):
        btn_gerar_split.disabled = True
        t.selected_index = 2
        progressBar_chunk.value = None
        progressBar_chunk.visible = True
        page.update()
        progressBar_chunk.update()
        tokens = tik_token.TikToken()
        text = ""
        doc = document_loader.DocumentLoader()
        chunk_overlap.update()

        if pagina.value:
            document_loaded = doc.filter_docs(doc.load_pdf(selected_files.value), pagina.value.split(','))
        else:
            document_loaded = doc.load_pdf(selected_files.value)

        doc_split = document_spliter.DocumentSpliter()
        result_split = doc_split.split_by_word(document_loaded, chunk_size=int(chunk_size.value),chunk_overlap=int(chunk_overlap.value))
        chunks=0

        vector_store.VectorStore().save_faiss(result_split)

        for split in result_split:
            time.sleep(0.2)
            num_tokens = tokens.num_tokens_from_string(split.page_content)
            chunks+=1
            text = text + '\n' + '-' * 90 + f' → chunk {chunks}' + '-' * 90 + f'\n 🪙 {num_tokens} \n' + split.page_content
            progressBar_chunk.value = 100 / len(result_split) / 100 * chunks
            progressBar_chunk.update()
            page.update()
        chunks_total.value = ' 🧩 '+str(chunks) + ' chunks.'
        container_2.content = ft.Text(text, selectable=True)
        page.window_maximized = False
        btn_gerar_split.disabled = False
        page.update()

    def send_click(e):
        user_message = new_message.value.strip()
        page.update()
        if user_message:
            chat.controls.append(ft.Container(ft.Text(f"Você: {user_message}", color=ft.colors.BLUE_700, selectable=True, left=True),alignment=ft.alignment.center_right, padding=10, bgcolor=ft.colors.BLUE_50, border_radius=10, margin=ft.margin.only(left=150)))
            numero_documentos.update()
            marginal.update()
            page.update()

            # Integre aqui a lógica de resposta do bot
            vector = vector_store.VectorStore().get_faiss()
            retriever = ia_retriever.IaRetriever(vector)
            score = ""
            rank = 0.0
            for i in retriever.get_similarity_with_relevance_scores(user_message, k=int(numero_documentos.value)):
                if i[1] > rank:
                    top = str(f'🎖️️ {i[1]} \n🎯{i[0].page_content}  \n\n')
                    rank = i[1]
                if i[1] > 0.5:
                    score = score + str(f'🎖️️ {i[1]} \n🎯{i[0].page_content}  \n\n')
            similarity = retriever.create_retriever_similarity(user_message)
            txt = ""
            for i in similarity:
                txt = txt + i.page_content

            marginal_similarity = retriever.get_similarity_with_max_marginal_relevance(user_message, k=int(numero_documentos.value), marginal=float(marginal.value))
            print(marginal.value)
            for m in marginal_similarity:
                print(m)

            bot_response = txt
            chat.controls.append(ft.Container(ft.Text(f"Bot: {top}", selectable=True, right=True), alignment=ft.alignment.bottom_left, padding=10,bgcolor=ft.colors.GREEN_50, border_radius=10,margin=ft.margin.only(right=150)))
            new_message.value = ""
            page.update()

    def clear(e):
        chat.controls.clear()
        page.update()

    page.add(ft.Text(f"", size=20, color='blue'))

    container_1 = ft.Container(content=ft.Text(""), alignment=ft.alignment.center, bgcolor=ft.colors.GREY_200,scale=1)
    btn_processar = ft.ElevatedButton("Processar...", on_click=btn_processar, icon=ft.icons.CHECK, visible=False, width=200)
    btn_gerar_split = ft.ElevatedButton("Iniciar Split", on_click=btn_chunk, icon=ft.icons.ADD_BOX)
    container_2 = ft.Container(content=ft.Text(""), alignment=ft.alignment.center, bgcolor=ft.colors.GREY_200, scale=1)
    chunk_size = ft.TextField(label="Tamanho da quebra (chunk)", value=2000)
    paginas_total = ft.Text('', size=20)
    tokens_total = ft.Text('Total tokens: 💰', size=20)
    chunks_total = ft.Text('', size=20)
    header = ft.Text("", size=20, color='blue')

    chat = ft.Column(scroll="always", expand=True, height=600)


    new_message = ft.TextField(hint_text="Digite sua pergunta aqui", autofocus=True, multiline=True)
    send_button = ft.ElevatedButton(text="Enviar", icon=ft.icons.SEND, on_click=send_click)
    btn_clear = ft.ElevatedButton(text="Limpar", icon=ft.icons.RECYCLING, on_click=clear)
    numero_documentos = ft.TextField(label='N° Doc', value=3, width=150)
    marginal = ft.TextField(label='Marginal Relevance',value=0.5, width=150)

    box_send_clear = ft.Row([send_button, btn_clear, marginal, numero_documentos])

    pagina = ft.TextField(label='Excluir páginas', width=150)
    chunk_overlap = ft.TextField(label='Overlap', value=25, width=150)


    t = ft.Tabs(
        selected_index=3,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Importar",
                icon=ft.icons.IMPORT_EXPORT,
                content=ft.Container(
                    content=ft.Column([btn_procurar_arquivo,pagina,progressBar, btn_processar]), alignment=ft.alignment.center, padding=15
                ),
            ),
            ft.Tab(
                text="Visualizar",
                icon=ft.icons.VIEW_COZY,
                content=ft.Container(content=ft.Column([header,tokens_total,paginas_total,btn_gerar_split,progressBar_chunk, container_1],scroll=True), alignment=ft.alignment.top_center, padding=15),
            ),
            ft.Tab(
                text="Chunks",
                icon=ft.icons.INSERT_PAGE_BREAK,
                content=ft.Container(content=ft.Column([header,chunk_overlap, btn_gerar_split, chunk_size, chunks_total,progressBar_chunk, container_2],scroll=True), alignment=ft.alignment.top_center, padding=20,
                ),
            ),
            ft.Tab(
                text="Chat",
                icon=ft.icons.CHAT,
                content=ft.Container(content=ft.Column([chat,new_message, box_send_clear], spacing=10), margin=ft.margin.all(20), alignment=ft.alignment.top_center),
            ),
        ],
        expand=1,
    )
    t.label_color='red'
    page.add(t)

if __name__ == "__main__":
    ft.app(target=pages)
    # ft.app(port=7000, target=pages, view=ft.WEB_BROWSER)

#  pyinstaller --name doc_valid --onefile --icon=.ico --noconsole page.py
# flet pack --name doc_split_V_1.0.0 --icon=icone_principal.ico page.py

# pyinstaller --add-data "C:\Users\Equiplano\PycharmProjects\doc_split\venvdoc_split\Lib\site-packages\langchain\chains\llm_summarization_checker\prompts\create_facts.txt;." --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext --console ./template/page.py

# pyinstaller --add-data "C:\Users\Equiplano\PycharmProjects\doc_split\venvdoc_split\Lib\site-packages\langchain\chains\llm_summarization_checker\prompts\create_facts.txt;." --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext --hidden-import=tqdm --hidden-import=sentence_transformers --console ./template/page.py

# pyinstaller --add-data "C:\Users\Equiplano\PycharmProjects\doc_split\venvdoc_split\Lib\site-packages\langchain\chains\llm_summarization_checker\prompts\create_facts.txt;." --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext --hidden-import=tqdm --hidden-import=sentence_transformers --hidden-import=transformers  --console ./template/page.py

# pyinstaller --add-data "C:\Users\Equiplano\PycharmProjects\doc_split\venvdoc_split\Lib\site-packages\langchain\chains\llm_summarization_checker\prompts\create_fact
# s.txt;." --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext --hidden-import=tqdm --hidden-import=sentence-transformers --hidden-import=transformers --hidden-import=langchain --hidden-import=huggingface-hub --console ./template/page.py
