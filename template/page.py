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

        for pag in doc.load_pdf(selected_files.value):
            paginas+=1
            num_tokens = tokens.num_tokens_from_string(pag.page_content)
            total_tokens+=num_tokens
            rest = doc.remove_crlf(pag.page_content)
            if doc_inf:
                text = text+'\n'+'-'*90 + ' → pagina ' +str(pag.metadata['page']+1) +'-'*90 +f'\n🪙 tokens:  {num_tokens}\n'+rest

        tokens_total.value = f'💰 {total_tokens} tokens total.\n 💵 '+ str((total_tokens / 1000) * 0.001) + ' custo.'
        paginas_total.value = f'📃 {paginas}'
        container_1.content=ft.Text(text, selectable=True)
        page.window_maximized = False
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
        page.window_maximized = False
        t.selected_index = 2
        page.update()

    def send_click(e):
        user_message = new_message.value.strip()
        page.update()
        if user_message:
            chat.controls.append(ft.Container(ft.Text(f"Você: {user_message}", color=ft.colors.BLUE_700, selectable=True, left=True),alignment=ft.alignment.center_right, padding=10, bgcolor=ft.colors.BLUE_50, border_radius=10, margin=ft.margin.only(left=150)))
            page.update()
            # Integre aqui a lógica de resposta do bot
            bot_response = "Resposta do bot"
            chat.controls.append(ft.Container(ft.Text(f"Bot: {bot_response}", color=ft.colors.GREEN_500,selectable=True, right=True), alignment=ft.alignment.bottom_left, padding=10,bgcolor=ft.colors.GREEN_50, border_radius=10,margin=ft.margin.only(right=150)))
            new_message.value = ""
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

    chat = ft.Column(scroll="always", expand=True, width=600, height=600, )

    new_message = ft.TextField(hint_text="Digite sua pergunta aqui", autofocus=True, width=600, multiline=True)
    send_button = ft.ElevatedButton(text="Enviar", icon=ft.icons.SEND, on_click=send_click)

    t = ft.Tabs(
        selected_index=3,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Importar",
                icon=ft.icons.IMPORT_EXPORT,
                content=ft.Container(
                    content=ft.Column([btn_procurar_arquivo,btn_processar]), alignment=ft.alignment.center, padding=15
                ),
            ),
            ft.Tab(
                text="Visualizar",
                icon=ft.icons.VIEW_COZY,
                content=ft.Container(content=ft.Column([header,tokens_total,paginas_total,btn_gerar_split, container_1],scroll=True), alignment=ft.alignment.top_center, padding=15),
            ),
            ft.Tab(
                text="Chunks",
                icon=ft.icons.INSERT_PAGE_BREAK,
                content=ft.Container(content=ft.Column([header,btn_gerar_split, chunk_size, chunks_total, container_2],scroll=True), alignment=ft.alignment.top_center, padding=20,
                ),
            ),
            ft.Tab(
                text="Chat",
                icon=ft.icons.CHAT,
                content=ft.Container(content=ft.Column([chat,new_message, send_button], spacing=10), margin=ft.margin.all(10), alignment=ft.alignment.top_center),
            ),
        ],
        expand=1,
    )
    t.label_color='red'
    page.add(t)


if __name__ == "__main__":
    ft.app(target=pages)
    # ft.app(port=3636, target=pages, view=ft.WEB_BROWSER)

#  pyinstaller --name export_conversor_frotas_sysmar --onefile --icon=transferencia-de-dados.ico --noconsole main.py
# flet pack --name doc_split_V_1.0.0 --icon=????.ico main.py