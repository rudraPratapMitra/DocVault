# from app.core.vector_store import create_collection,index_document
# create_collection()
# chunks = [
#     "SQL retrieves data from databases",
#     "WHERE filters rows",
#     "SELECT fetches records"
# ]

# count = index_document(
#     document_id=1,
#     owner_id=1,
#     chunks=chunks
# )

# print(count)

from app.core.vector_store import search_chunks


results = search_chunks(
    query="What is SQL?",
    owner_id=1,
    document_id=3
)

print(results)