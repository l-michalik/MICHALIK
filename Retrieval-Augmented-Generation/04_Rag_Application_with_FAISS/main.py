import os
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

document = TextLoader('rowdata.txt', encoding='utf-8').load()

text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
text_chunks=text_splitter.split_documents(document)

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = FAISS.from_documents(text_chunks, embeddings)
retriever = vectorstore.as_retriever()

from langchain.prompts import ChatPromptTemplate

templete="""You are an assistant for question answering tasks.
You will be provided with a question and some context.
Use the context to answer the question. 
If the context does not provide enough information, say "I don't know".
Question: {question}
Context: {context}
Answer:
"""

prompt = ChatPromptTemplate.from_template(templete)

output_parser = StrOutputParser()

llm_model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4o-mini", temperature=0)

rag_chain = (
    { "context": retriever, "question": RunnablePassthrough() }
    | prompt
    | llm_model
    | output_parser
)

res = rag_chain.invoke("What did the president say about Ketanji Brown Jackson?")

print(res)