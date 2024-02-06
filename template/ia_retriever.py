from langchain.retrievers import BM25Retriever, EnsembleRetriever
class IaRetriever:

    def __init__(self, vectordb):
        self.vectordb = vectordb
        self.bm25_retriever = None
        self.retriever = None

    def create_retriever(self):
        self.retriever = self.vectordb.as_retriever()
        print(self.retriever)
        return self.retriever

    def create_retriever_similarity(self, question):
        self.retriever = self.vectordb.similarity_search(question)
        return self.retriever

    def create_bm25_retriever(self, documents):
        self.bm25_retriever = BM25Retriever.from_documents(documents=documents)
        self.bm25_retriever.k = 7
        return self.bm25_retriever

    def create_ensemble(self, bm25_retriever, retriever, query):
        ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever], weights=[0.5, 0.5])
        return ensemble_retriever.get_relevant_documents(query=query)

    def create_similarity_score_retriever(self):
        similarity_score_retriever = self.vectordb.as_retriever(search_type="mmr", search_kwargs={'fetch_k': 30})
        return similarity_score_retriever

    def create_retriever_query(self, query):
        retriever = self.vectordb.similarity_search(query)
        return retriever

    def get_similarity_with_relevance_scores(self, consulta, k=3):
        retriever = self.vectordb.similarity_search_with_relevance_scores(consulta, k=k)
        return retriever

    def get_similarity_with_max_marginal_relevance(self, consulta, k=5, marginal=0.5):
        retriever = self.vectordb.max_marginal_relevance_search(consulta, k=k, marginal=marginal)
        return retriever

    def get_max_marginal_relevance_search_with_score_by_vector(self, consulta, k=5, diversidade=0.5):
        retriever = self.vectordb.max_marginal_relevance_search_with_score_by_vector(consulta, k=k, lambda_mult=diversidade)
        return retriever


