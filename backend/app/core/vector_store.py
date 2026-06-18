from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams,Distance,PointStruct,Filter,FieldCondition,MatchValue
from app.core.embeddings import generate_embedding
import uuid
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
def index_document(document_id: int,owner_id: int,chunks: list[str]):
    points=[]
    for chunk in chunks:
        embedding=generate_embedding(chunk)
        point=PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding.tolist(),
            payload={
                "document_id":document_id,
                "owner_id":owner_id,
                "chunk_text":chunk
            }
        )
        points.append(point)
    client.upsert(  
        collection_name="docvault_chunks",
        points=points
    )
    return len(points)

def search_chunks(query:str, owner_id: int,document_id: int):
    query_embedding=generate_embedding(query)
    results=client.query_points(
        collection_name="docvault_chunks",
        query=query_embedding.tolist(),
        query_filter=Filter(
            must=[
            FieldCondition(
                key="owner_id",
                match=MatchValue(value=owner_id)
            ),
            FieldCondition(
                key="document_id",
                match=MatchValue(value=document_id)
            )
        ]
        ),
        limit=3
        )
    chunks = []
    for point in results.points:
        chunks.append(
            point.payload["chunk_text"]
        )

    return chunks
