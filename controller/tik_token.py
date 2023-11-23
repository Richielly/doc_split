import tiktoken

class TikToken:
    def __init__(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.encoding_model = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def num_tokens_from_string(self, string: str) -> int:
        """Retorna o número de tokens em uma sequência de texto."""
        encoding = tiktoken.get_encoding(self.encoding_model.name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
