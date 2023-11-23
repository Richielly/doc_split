import os

import flet as ft
from controller import document_loader, document_spliter, tik_token

def pages(page: ft.Page):

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_center()
    page.title = "Gerenciador de arquivos IA" + " V_1.0.0"
    page.icon = "imagem_principal.png"
    progressBar = ft.ProgressBar(width=700, color=ft.colors.DEEP_ORANGE)

    def pick_files_result(e: ft.FilePickerResultEvent):

        selected_files.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelado!"
        )
        selected_files.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    page.overlay.append(pick_files_dialog)

    btn_procurar_arquivo = (
        ft.Row(
            [
                ft.ElevatedButton(
                    "Arquivo",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),
                ),
                selected_files,
            ]
        )
    )

    def btn_click(e):
        resulta_data = []
        text = ""
        doc_inf = True
        doc = document_loader.DocumentLoader()
        tokens = tik_token.TikToken()
        total_tokens=0
        paginas = 0

        for pag in doc.load_pdf(selected_files.value):
            paginas+=1
            num_tokens = tokens.num_tokens_from_string(pag.page_content)
            total_tokens+=num_tokens
            if doc_inf:
                text = text+'\n'+'-'*90 + ' → pagina ' +str(pag.metadata['page']+1) +'-'*90 +'\n'+pag.page_content +f'\n 🪙 tokens:  {num_tokens}\n'
        tokens_total.value = f'💰 {total_tokens} \n 💵 '+ str((total_tokens / 1000) * 0.001)
        paginas_total.value = f'📃 {paginas}'
        container_1.content=ft.Text(text, selectable=True)
        t.selected_index=1
        page.update()

    def btn_chunk(e):
        tokens = tik_token.TikToken()
        text = ""
        doc = document_loader.DocumentLoader()
        document_loaded = doc.load_pdf(selected_files.value)
        doc_split = document_spliter.DocumentSpliter()
        result_split = doc_split.split_by_word(document_loaded, chunk_size=int(chunk_size.value))
        chunks=0

        for split in result_split:
            num_tokens = tokens.num_tokens_from_string(split.page_content)
            chunks+=1
            text = text + '\n' + '-' * 90 + f' → chunk {chunks}' + '-' * 90 + f'\n 🪙 {num_tokens} \n' + split.page_content
        chunks_total.value = ' 🧩 '+str(chunks) + ' chunks.'
        container_2.content = ft.Text(text, selectable=True)
        # print(split.page_content)
        t.selected_index = 2
        page.update()


    page.add(ft.Text(f"Resultado ", size=20, color='blue'))

    container_1 = ft.Container(content=ft.Text(""), alignment=ft.alignment.center, bgcolor=ft.colors.GREY_200,scale=1)
    btn_gerar_arquivos = ft.ElevatedButton("Gerar Arquivos", on_click=btn_click, icon=ft.icons.ADD_BOX)
    btn_gerar_split = ft.ElevatedButton("Iniciar Split", on_click=btn_chunk, icon=ft.icons.ADD_BOX)
    container_2 = ft.Container(content=ft.Text(""), alignment=ft.alignment.center, bgcolor=ft.colors.GREY_200, scale=1)
    chunk_size = ft.TextField(label="Tamanho da quebra (chunk)", value=2000)
    paginas_total = ft.Text('', size=30)
    tokens_total = ft.Text('Total tokens: 💰', size=30)
    chunks_total = ft.Text('', size=30)
    header = ft.Text("Pagina", size=20, color='blue')

    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Importar",
                icon=ft.icons.IMPORT_EXPORT,
                content=ft.Container(
                    content=ft.Column([header,btn_procurar_arquivo,btn_gerar_arquivos]), alignment=ft.alignment.center, padding=15
                ),
            ),
            ft.Tab(
                text="Visualizar",
                icon=ft.icons.VIEW_COZY,
                content=ft.Container(content=ft.Column([header,tokens_total,paginas_total,btn_gerar_split, container_1],scroll=True), alignment=ft.alignment.center, padding=15),
            ),
            ft.Tab(
                text="Chunks",
                icon=ft.icons.INSERT_PAGE_BREAK,
                content=ft.Container(
                    content=ft.Column([header,btn_gerar_split, chunk_size, chunks_total, container_2],scroll=True), alignment=ft.alignment.center, padding=15
                ),
            ),
        ],
        expand=1,
    )

    page.add(t)

if __name__ == "__main__":
    ft.app(target=pages)

#  pyinstaller --name export_conversor_frotas_sysmar --onefile --icon=transferencia-de-dados.ico --noconsole main.py
# flet pack --name doc_split_V_1.0.0 --icon=????.ico main.py