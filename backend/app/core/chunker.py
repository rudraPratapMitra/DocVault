from langchain_text_splitters import RecursiveCharacterTextSplitter

# def chunk_text(text:str,chunk_size:int=100,overlap: int = 20):
#     chunks=[]
#     for i in range(0,len(text),chunk_size-overlap):
#         chunk=text[i:i+chunk_size]
#         chunks.append(chunk)
#     return chunks

def chunk_text(text:str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_text(text)

    return chunks