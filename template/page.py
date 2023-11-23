import os

import flet as ft
from controller import document_loader

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
        chunk = 0
        doc = document_loader.DocumentLoader()
        for pag in doc.load_pdf(selected_files.value):
            chunk+=1
            text = text+'\n'+'-'*50 + 'Chunk: '+ str(chunk) +'-'*50 +'\n'+pag.page_content

        container_1.content=ft.Text(text, selectable=True)
        t.selected_index=1
        page.update()

        # if not txt_database.value:
        #     txt_database.error_text = "Informe o caminho do Banco"
        #     page.update()
        # else:
        #     page.update()

    page.add(ft.Text(f"Resultado ", size=20, color='blue'))
    # header_frotas = ft.Text("Gerador de Arquivos das Frotas", size=20, color='blue')
    # txt_entidade = ft.TextField(label="Entidade", text_size=12, value=cfg['DEFAULT']['CodEntidade'], width=100, height=35, disabled=False, tooltip='Alterar o código de entidade, tambem altera o arquivo "cfg.ini"')
    # txt_password = ft.TextField(label="Password", text_size=12, value=cfg['DEFAULT']['password'], width=130, height=35, password=True, can_reveal_password=True)

    container_1 = ft.Container(content=ft.Text("Center"), alignment=ft.alignment.center, bgcolor=ft.colors.GREY_200,scale=1)
    btn_gerar_arquivos = ft.ElevatedButton("Gerar Arquivos", on_click=btn_click, icon=ft.icons.ADD_BOX)
    # list_arquivos = ft.ListView(expand=1, spacing=2, padding=20, auto_scroll=True)
    # divisor = ft.Divider(height=2, thickness=3)

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
                content=ft.Container(content=ft.Column([header,container_1],scroll=True), alignment=ft.alignment.center, padding=15),
            ),
            ft.Tab(
                text="Configurações",
                icon=ft.icons.ADMIN_PANEL_SETTINGS,
                content=ft.Container(
                    content=ft.Column([header]), alignment=ft.alignment.center, padding=15
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