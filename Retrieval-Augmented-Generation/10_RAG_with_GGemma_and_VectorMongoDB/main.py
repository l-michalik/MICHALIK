from datasets import load_dataset
import pandas as pd

dataset = load_dataset("MongoDB/embedded_movies", split="train")

data = pd.DataFrame(dataset)

data = data.dropna(subset=['fullplot'])

data = data.drop(columns=['plot_embedding'])

from sentence_transformers import SentenceTransformer
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_embeddings(text:str) -> list:
    if not text.strip():
        return []
    
    embedding = embedding_model.encode(text)
    return embedding.tolist()

data['embedding'] = data['fullplot'].apply(lambda x: get_embeddings(x))

print(data['embedding'])
