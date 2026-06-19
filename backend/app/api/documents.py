from fastapi import APIRouter, Depends, HTTPException, UploadFile,File
from sqlalchemy.orm import Session
import os
from app.models.document import Document
from app.core.dependencies import get_db
from app.schemas.document import DocumentResponse
from app.core.oauth2 import get_current_user
from app.models.user import User
from app.core.chunker import chunk_text
from app.core.pdf import extract_text_from_pdf
from app.core.vector_store import create_collection, index_document
from app.schemas.query import QueryRequest, QueryResponse
from app.core.vector_store import search_chunks
from app.core.llm import generate_answer
router = APIRouter()
MAX_FILE_SIZE = 10 * 1024 * 1024

@router.post("/documents")
def upload_document(file:UploadFile=File(...),db: Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    file_path=f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    
    file_content = file.file.read()
    content_type = file.content_type
    file_size = len(file_content)

    
    if file_size==0:
        raise HTTPException(
            status_code=400,
            detail="File cannot be empty"
        )
    if content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    if file_size>MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds limit"
        )
    with open(file_path,"wb") as buffer:
        buffer.write(file_content)

    document = Document(
        filename=file.filename,
        owner_id=current_user.id,
        file_path=file_path,
        content_type=content_type,
        file_size = file_size,
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)

    create_collection()
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    indexed_chunks = index_document(
        document_id=document.id,
        owner_id=current_user.id,
        chunks=chunks,
    )
    return{
        "id":document.id,
        "filename":document.filename,
        "status":document.status,
        "chunks_indexed": indexed_chunks
    }
@router.get("/documents")
def get_my_documnets(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    documents=db.query(Document).filter(Document.owner_id==current_user.id).all()
    return documents

@router.get("/documents/{document_id}",response_model=DocumentResponse)
def find_documnt_by_id(document_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    document=db.query(Document).filter(Document.id==document_id).first()
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    if document.owner_id!=current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )
    return document

@router.delete("/documents/{document_id}")
def delete_document(document_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    document=db.query(Document).filter(Document.id==document_id).first()
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    if document.owner_id!=current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )
    db.delete(document)
    db.commit()
    return {
        "message":f"Document {document_id} deleted"
    }

@router.post("/documents/{document_id}/query",response_model=QueryResponse)
def query_document(document_id:int,request:QueryRequest,db: Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    document=db.query(Document).filter(Document.id==document_id).first()
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    if document.owner_id!=current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )
    chunks=search_chunks(
        query=request.question,
        owner_id=current_user.id,
        document_id=document_id
        )
    answer = generate_answer(
        question=request.question,
        chunks=chunks
    )   
    return QueryResponse(
        answer=answer
    )