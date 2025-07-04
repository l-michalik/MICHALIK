from sentence_transformers import SentenceTransformer
from typing import Union, List

_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
    return _model.encode(text).tolist()
