import os
import torch
from dotenv import load_dotenv
from huggingface_hub import login

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate, ServiceContext
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("Missing HuggingFace API key in environment (HF_API_KEY)")

login(token=HF_API_KEY)

documents = SimpleDirectoryReader("data").load_data()

system_prompt = PromptTemplate("You are an expert in answering questions as accurately as possible based on the provided context.")
query_wrapper_prompt = PromptTemplate("<|USER|>{query}<|ASSISTANT|>")

llm = HuggingFaceLLM(
    context_window=4096,
    max_new_tokens=256,
    generate_kwargs={"temperature": 0.1, "do_sample": False},
    system_prompt=system_prompt,
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name="mistralai/Mistral-7B-Instruct-v0.1",
    model_name="mistralai/Mistral-7B-Instruct-v0.1",
    device_map="auto",
    stopping_ids=[50278, 50279, 50277, 1, 0],
    tokenizer_kwargs={"max_length": 4096},
    model_kwargs={"torch_dtype": torch.bfloat16},
)

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

service_context = ServiceContext.from_defaults(
    chunk_size=1024,
    llm=llm,
    embed_model=embed_model,
)

index = VectorStoreIndex.from_documents(
    documents,
    service_context=service_context,
)

query_engine = index.as_query_engine()

response = query_engine.query("What is RAG?")
print(response)