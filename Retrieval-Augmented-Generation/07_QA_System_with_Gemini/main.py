import os
import google.generativeai as genai # type: ignore

from dotenv import load_dotenv # type: ignore
from llama_index.llms.gemini import Gemini # type: ignore
from llama_index.core import SimpleDirectoryReader # type: ignore
from llama_index.core import VectorStoreIndex # type: ignore
from IPython.display import Markdown, display # type: ignore
from llama_index.core import ServiceContext # type: ignore
from llama_index.core import StorageContext, load_index_from_storage # type: ignore
from llama_index.embeddings.gemini import GeminiEmbedding # type: ignore

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

for models in genai.list_models():
    if 'generateContent' in models.supported_generation_methods:
        print(f"Model: {models.name}")