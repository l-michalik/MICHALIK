from haystack.document_stores.in_memory import InMemoryDocumentStore
from datasets import load_dataset
from haystack import Document
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.retrievers import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack import Pipeline
from dotenv import load_dotenv
import os

document_store = InMemoryDocumentStore()
data = load_dataset("bilgeyucel/seven-wonders", split="train")

docs = [Document(content=doc["content"], meta=doc["meta"]) for doc in data]

doc_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
doc_embedder.warm_up()
embedded_docs_output = doc_embedder.run(docs)

embedded_docs = embedded_docs_output["documents"]
document_store.write_documents(embedded_docs)

text_embedder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
retriever = InMemoryEmbeddingRetriever(document_store=document_store)

template = """
You are an expert in the Seven Wonders of the Ancient World.
Answer the question based on the context.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{question}}
Answer:
"""

prompt_builder = PromptBuilder(
    template=template,
    required_variables=["documents", "question"]
)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")

from haystack.utils import Secret

llm = OpenAIGenerator(
    model="gpt-3.5-turbo",
    api_key=Secret.from_token(OPENAI_API_KEY),
)

basic_rag_pipeline = Pipeline()
basic_rag_pipeline.add_component("text_embedder", text_embedder)
basic_rag_pipeline.add_component("retriever", retriever)
basic_rag_pipeline.add_component("prompt_builder", prompt_builder)
basic_rag_pipeline.add_component("llm", llm)

basic_rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
basic_rag_pipeline.connect("retriever.documents", "prompt_builder.documents")
basic_rag_pipeline.connect("prompt_builder", "llm")

question = "What are the Seven Wonders of the Ancient World?"

response = basic_rag_pipeline.run({
    "text_embedder": {"text": question},
    "prompt_builder": {"question": question}
})

print(response["llm"]["replies"][0])
