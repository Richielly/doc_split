import llm_factory
import os

# os.environ["OPENAI_MODEL_NAME"]="gpt-3.5-turbo-0125"
# os.environ["SERPER_API_KEY"] = "Your Key" # serper.dev API key
# from openai import OpenAI

#Para utilizar llm local
# os.environ["OPENAI_API_BASE"]="http://localhost:1234/v1"
# os.environ["OPENAI_MODEL_NAME"]="local-model"
# os.environ["OPENAI_API_KEY"]="not-needed"

from crewai import Agent, Task, Crew
# from crewai_tools import SerperDevTool
# my_llm = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

class CrewAI:

    def agent_build(self):

        agent = Agent(role='Customer Support',
                      goal='Analise esta resposta """{resposta}"""" que foi fornecida ao cliente para a pergunta a seguir, Pergunta: {pergunta}',
                      backstory="""Você é atendente de suporte em uma grande empresa.
                      Você é responsável por receber as demandas de duvidas dos clientes, analisar e fornecer a melhor resposta.
                      Você está atualmente trabalhando em um chat de atendimento e é responsavel por analisar a pergunta verificar se pode ser respondida adequadamente.""",
                      llm=llm_factory.LlmFactory().create_llm,  # Optional
                      verbose=True  # Optional
                      )
        return agent
# search_tool = SerperDevTool()

    def task_build(self, agent):
        task = Task(description='Crie um passo a passo para responder a pergunta.',
                    expected_output='Instruções detalhadas sobre a pergunta recebida, na lingua portuguêsa pt-BR, deixe sempre em destaque o caminho para chegar a funcionalidade quando houver.',
                    #expected_output='Informe o caminho do menu para a funcionalidade apenas.',
                    agent=agent,
                    #tools=[search_tool]
                    )
        return task
    def get_crew(self):
        agent = self.agent_build()
        task = self.task_build(agent=agent)
        crew = Crew(agents=[agent],
                    tasks=[task],
                    verbose=2
                    )
        return crew
    def response_crew(self, pergunta, resposta):
        crew = self.get_crew()
        result = crew.kickoff(inputs={'resposta': f'{resposta}', 'pergunta': f'{pergunta}'})
        return result



pergunta = "como cadastrar uma tabela de ir"
resposta = """ A funcionalidade para cadastrar a tabela de IR está disponível em Cadastros > Tabelas > IR. Na tela de cadastro, é possível inserir as informações de cada faixa de IR, como o valor do limite inferior e superior, a alíquota correspondente e a dedução. Após preencher todas as informações, selecione o botão Gravar para concluir o cadastro da tabela de IR. """
#
print(CrewAI().response_crew(pergunta=pergunta, resposta=resposta))