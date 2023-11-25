from controller.vector_store import VectorStore
from controller.ia_retriever import IaRetriever
from controller.prompt_template import Prompt_Template
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from controller.llm_factory import LlmFactory

llm_factory = LlmFactory()
llm=llm_factory.create_llm(model='gpt_3.5')
prompt_template = Prompt_Template()
class Chat:

    def chat_session(self, question):
        dbvector = VectorStore()
        vector = dbvector.get_faiss()
        ia_retriever = IaRetriever(vector)
        _retriever = ia_retriever.create_retriever()

        resposta = vector.similarity_search(query=question)

        template = prompt_template.get_qa_template('1')

        prompt=PromptTemplate.from_template(template=template)

        llmquery = LLMChain(llm=llm, prompt=prompt)

        response = llmquery.run({'context': resposta, 'question': question})

        return response

t = Chat()

t.chat_session('teste')