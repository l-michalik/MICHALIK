from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    WEAVIATE_REST_ENDPOINT = os.getenv("WEAVIATE_REST_ENDPOINT")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
