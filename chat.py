import flet as ft

def main(page: ft.Page):
    page.title = "Chat com Bot"
    page.vertical_alignment = "start"

    chat = ft.Column(scroll="always", expand=True)

    new_message = ft.TextField(hint_text="Digite sua pergunta aqui", autofocus=True, width=300)
    send_button = ft.ElevatedButton(text="Enviar", icon=ft.icons.SEND, on_click=lambda e: send_click())

    def send_click():
        user_message = new_message.value.strip()
        if user_message:
            chat.controls.append(ft.Text(f"Você: {user_message}", color=ft.colors.BLUE))
            # Integre aqui a lógica de resposta do bot
            bot_response = "Resposta do bot"
            chat.controls.append(ft.Text(f"Bot: {bot_response}", color=ft.colors.GREEN))
            new_message.value = ""
            page.update()

    page.add(
        chat,
        ft.Row(controls=[new_message, send_button], alignment="center", spacing=10)
    )

ft.app(target=main)
