from weaviate.classes.config import Property, DataType, Configure # type: ignore
from weaviate.classes.init import Auth # type: ignore
import weaviate # type: ignore

from utils.config import Config

_weaviate_client: weaviate.WeaviateClient | None = None

def get_weaviate_client() -> weaviate.WeaviateClient:
    global _weaviate_client
    if _weaviate_client is None:
        _weaviate_client = weaviate.connect_to_weaviate_cloud(
            cluster_url=Config.WEAVIATE_REST_ENDPOINT,
            auth_credentials=Auth.api_key(Config.WEAVIATE_API_KEY),
        )
    return _weaviate_client

def create_schema_if_missing(client: weaviate.WeaviateClient) -> None:
    class_name = "DocChunk"

    if not client.collections.exists(class_name):
        print(f"Collection '{class_name}' does not exist. Creating it...")
        client.collections.create(
            name=class_name,
            properties=[
                Property(name="content", data_type=DataType.TEXT),
                Property(name="source", data_type=DataType.TEXT),
            ],
            vectorizer_config=Configure.Vectorizer.none()
        )
        print(f"Collection '{class_name}' created successfully.")
