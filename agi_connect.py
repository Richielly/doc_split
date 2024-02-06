import os
from pathlib import Path
import PIL.Image
import cohere
import google.generativeai as genai

GOOGLE_API_KEY='AIzaSyBhZwNJ2aEjZh39Dewd5K3Pq-GIoQfHXZ8'

genai.configure(api_key=GOOGLE_API_KEY)
class AgiConnect:
    def talk(self, texto, pergunta):
        co = cohere.Client("QnslN6ws6Z0Mf8Z2trkbtmoN4VU3z29yh0NKpf3J")

        response = co.generate(
        prompt=f'''A sua tarefa é analisar o texto criticamente e responder o que esta na pergunta.
        texto: """ {texto} """ 
        pergunta: {pergunta}
        - responda apenas o que foi perguntado
        - a resposta deve ser em português do Brasil.
        resposta:''',
        )
        return response[0]

    def image_talk(self):
        pass

        # for m in genai.list_models():
        #     if 'generateContent' in m.supported_generation_methods:
        #         print(m.name)
        # model = genai.GenerativeModel('gemini-pro')
        # response = model.generate_content("Qual o sentido da vida?", stream=True)
        #
        # for chunk in response:
        #     print(chunk.text)
        #     print("_" * 80)

        # model = genai.GenerativeModel('gemini-pro-vision')
        # img = PIL.Image.open('placa-do-onix.png')
        # response = model.generate_content(["qual a placa deste veiculo?, responda com calma, analise bem principalmente as letras, caso tenha duvida revise quantas vesez for necessário para responder corretamente.", img])
        # response.resolve()
        # print(response.text)

        # model = genai.GenerativeModel('gemini-pro')
        # chat = model.start_chat(history=[])
        #
        # response = chat.send_message("Qual a melhor inteligencias.")
        # print(response.text)

        # print(chat.history)

        # model = genai.GenerativeModel('gemini-pro-vision')
        #
        # cookie_picture = [{
        #     'mime_type': 'image/png',
        #     'data': Path('imagem_principal.png').read_bytes()
        # }]
        # prompt = "quais os dados mais importantes desta imagem?"
        #
        # response = model.generate_content(
        #     model="gemini-pro-vision",
        #     contents=[prompt, cookie_picture]
        # )
        # print(response.text)



# t = AgiConnect()
# t.image_talk()
#
# texto = """ Módulo Contábil > Configurações Gerais > Parâmetros Contas de Resultado
#     Permite relacionar as Contas de Resultado do Exercício por Entidade.
#     Após preencher os campos, clicar na opção Salvar. """
#
# pergunta = """ qual menu para a funcionalidade? """
#
# print(t.talk(texto=texto, pergunta=pergunta))
