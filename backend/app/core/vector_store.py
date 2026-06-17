from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams,Distance,PointStruct
from app.core.embeddings import generate_embedding
client=QdrantClient(
    path="./qdrant_data"
)
def get_qdrant_client():
    return client

def create_collection():
    if not client.collection_exists("docvault_chunks"):
        client.create_collection(
            collection_name="docvault_chunks",
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )