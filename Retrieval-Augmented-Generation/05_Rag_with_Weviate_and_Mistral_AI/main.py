import weaviate
import warnings
import locale
import os

from dotenv import load_dotenv
from weaviate.classes.init import Auth
from langchain_huggingface import HuggingFaceEmbeddings # type: ignore
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from weaviate.classes.config import Property, DataType
from langchain.prompts import ChatPromptTemplate
from langchain_community.retrievers import WeaviateHybridSearchRetriever
from weaviate.classes.init import Auth
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_community.llms import HuggingFaceHub
from langchain.schema import Document

warnings.filterwarnings("ignore")

load_dotenv()

WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    headers={'X-OpenAI-Api-key': OPENAI_API_KEY}
)

locale.getpreferredencoding = lambda: 'UTF-8'

embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model_name
)

loader = PyPDFLoader("./rag.pdf", extract_images=True)
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20
)

docs = text_splitter.split_documents(pages)

print(f"Number of documents: {len(docs)}")

collection = client.collections.get("rag_knowledge_base")

if not collection.name:
    client.collections.create(
    name="rag_knowledge_base",
    properties=[
        Property(name="text", data_type=DataType.TEXT),
        Property(name="vectorizer_config", data_type=DataType.TEXT)
    ])
    
    collection = client.collections.get("rag_knowledge_base")
    
texts = [doc.page_content for doc in docs]
vectors = embeddings.embed_documents(texts)

for text, vector in zip(texts, vectors):
    collection.data.insert(
        properties={"text": text},
        vector=vector
    )
    
query = "What is rag?"
query_vector = embeddings.embed_query(query)

results = collection.query.near_vector(
    near_vector=query_vector,
    limit=3
)

retrieved_docs = [
    Document(page_content=obj.properties["text"], metadata={})
    for obj in results.objects
]

context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

prompt_template = """
You are an AI assistant specialized in answering questions based on the provided context.
Use the following pieces of context to answer the question at the end.
Context: {context}
Question: {question}
Answer:
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

model = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    huggingfacehub_api_token=HUGGINGFACE_API_KEY,
    model_kwargs={"temperature": 1, "max_new_tokens": 200}
)

output_parser = StrOutputParser()

from langchain_core.runnables import RunnableLambda

chain = (
    {
        "context": RunnableLambda(lambda _: context_text), 
        "question": RunnablePassthrough()                    
    }
    | prompt                                                  
    | model 
    | output_parser
)

response = chain.invoke("What is rag?")

print(f"Response: {response}")

client.close()