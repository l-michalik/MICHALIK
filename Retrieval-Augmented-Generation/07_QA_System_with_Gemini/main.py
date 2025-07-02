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
        
documents = SimpleDirectoryReader('../data').load_data()

model = Gemini(models='gemini-1.5-pro', api_key=GOOGLE_API_KEY)

# Split the documents into smaller chunks to avoid exceeding the payload size limit
from llama_index.core import Document

# Define a function to split large documents into smaller chunks
def split_documents(documents, max_chunk_size=1000):
	split_docs = []
	for doc in documents:
		content = doc.text
		for i in range(0, len(content), max_chunk_size):
			chunk = content[i:i + max_chunk_size]
			split_docs.append(Document(text=chunk, metadata=doc.metadata))
	return split_docs

# Split the documents
split_docs = split_documents(documents)

# Use the smaller chunks for embedding
gemini_embed_model = GeminiEmbedding(model_name='models/gemini-1.5-pro', nodes=split_docs)

from llama_index.core import Settings

Settings.embed_model = gemini_embed_model

index = VectorStoreIndex.from_documents(split_docs, embed_model=gemini_embed_model)

index.storage_context.persist()

# Ensure the query engine is initialized with the correct settings
query_engine = index.as_query_engine(llm=model)

query_engine.query("What is the main topic of the documents?")