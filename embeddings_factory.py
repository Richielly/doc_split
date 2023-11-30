from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
class EmbeddingsFactory:

    def __init__(self):
        self.embedding = None

    def get_embeddings(self):
        self.embedding = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2")

        return self.embedding