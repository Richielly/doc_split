from langchain.chat_models import ChatOpenAI
from langchain.llms import LlamaCpp
from langchain.llms import GPT4All
from functools import lru_cache

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class LlmFactory:

    def __init__(self):
        pass

    @lru_cache(maxsize=32)
    def create_llm(self, model='llama-7b_GPU', temperature: float = 0.0):
        match model:
            case 'gpt_3.5':
                self.llm = ChatOpenAI(openai_api_key="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", model='gpt-3.5-turbo-0301', streaming=True)

            case 'llama-7b':
                self.llm = LlamaCpp(model_path="./llm/models/llama-2-7b-chat.ggmlv3.q8_0.bin", verbose=True, n_ctx=6000, top_p=0.7, temperature=temperature, streaming=True)

            case 'llama-13b':
                self.llm = LlamaCpp(model_path="./llm/models/llama-2-13b-chat.ggmlv3.q8_0.bin", verbose=True, n_ctx=6000, top_p=0.7, temperature=temperature, streaming=True)

            case 'llama-7b_GPU':
                # Callbacks support token-wise streaming
                callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
                n_gpu_layers = 20  # Change this value based on your model and your GPU VRAM pool.
                n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
                self.llm = LlamaCpp(model_path="./llm/models/llama-2-7b-chat.Q4_K_M.gguf",
                                    verbose=True,
                                    n_ctx=6000,
                                    top_p=0.7,
                                    temperature=temperature,
                                    streaming=True,
                                    n_gpu_layers=n_gpu_layers,
                                    n_batch=n_batch,
                                    callback_manager=callback_manager)

            case 'llama-13b_GPU':
                # Callbacks support token-wise streaming
                callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
                n_gpu_layers = 15  # Change this value based on your model and your GPU VRAM pool.
                n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
                self.llm = LlamaCpp(model_path="./llm/models/llama-2-13b.Q4_0.gguf",
                                    verbose=True,
                                    n_ctx=6000,
                                    top_p=0.7,
                                    temperature=temperature,
                                    streaming=True,
                                    n_gpu_layers=n_gpu_layers,
                                    n_batch=n_batch,
                                    callback_manager=callback_manager)

            case 'gpt4all':
                self.llm = GPT4All(model="./llm/models/ggml-model-gpt4all-falcon-q4_0.bin", max_tokens=2048)

        return self.llm