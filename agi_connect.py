import cohere

class AgiConnect:
    def talk(self, texto, pergunta):
        co = cohere.Client("")

        response = co.generate(
        prompt=f'''A sua tarefa é analisar o texto criticamente e responder o que esta na pergunta.
        texto: """ {texto} """ 
        pergunta: {pergunta}
        - responda apenas o que foi perguntado
        - a resposta deve ser em português do Brasil.
        resposta:''',
        )
        return response[0]


# t = AgiConnect()
#
# texto = """ Módulo Contábil > Configurações Gerais > Parâmetros Contas de Resultado
#     Permite relacionar as Contas de Resultado do Exercício por Entidade.
#     Após preencher os campos, clicar na opção Salvar. """
#
# pergunta = """ qual menu para a funcionalidade? """
#
# print(t.talk(texto=texto, pergunta=pergunta))