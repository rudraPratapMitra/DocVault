# from app.core.pdf import extract_text_from_pdf
# from app.core.chunker import chunk_text
# pdf="uploads/01_SQL_Introduction.pdf"

# text=extract_text_from_pdf(pdf)
# text_len=len(text)
# chunks=chunk_text(text)
# print(text_len)
# print(len(chunks))

from app.core.embeddings import generate_embedding

# embedding = generate_embedding(
#     "SQL retrieves data"
# )

# print(type(embedding))
# print(len(embedding))
# print(embedding[:10])

from qdrant_client import QdrantClient
client=QdrantClient(":memory:")
from qdrant_client.models import VectorParams, Distance,PointStruct

client.create_collection(
    collection_name="docvault_chunks",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

texts = [
    "SQL retrieves data from databases",
    "Python is a programming language",
    "FastAPI is used to build APIs"
]
for idx,text in enumerate(texts,start=1):
    embedding=generate_embedding(text)
    client.upsert(
        collection_name="docvault_chunks",
        points=[
            PointStruct(
                id=idx,
                vector=embedding.tolist(),
                payload={
                    "text":text
                }
            )
        ]
    )
query = "How do I query data?"
query_embedding = generate_embedding(query)
results = client.query_points(
    collection_name="docvault_chunks",
    query=query_embedding.tolist(),
    limit=3
)

print(results)
for point in results.points:
    print(point.score)
    print(point.payload)
    print()