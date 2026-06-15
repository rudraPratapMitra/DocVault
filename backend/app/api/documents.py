from fastapi import APIRouter, Depends, HTTPException, UploadFile,File
from sqlalchemy.orm import Session
import os
from app.models.document import Document
from app.core.dependencies import get_db
from app.schemas.document import DocumentResponse

router = APIRouter()

@router.post("/documents")
def upload_document(file:UploadFile=File(...),db: Session = Depends(get_db)):
    file_path=f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_path,"wb") as buffer:
        buffer.write(file.file.read())

    document = Document(
        filename=file.filename,
    )

    db.add(document)
    db.commit()
    db.refresh(document)
    return{
        "id":document.id,
        "filename":document.filename,
        "status":document.status
    }
@router.get("/documets")
def get_all_documnets(db:Session=Depends(get_db)):
    documents=db.query(Document).all()
    return documents

@router.get("/documnets/{document_id}",response_model=DocumentResponse)
def find_documnt_by_id(document_id:int,db:Session=Depends(get_db)):
    documnet=db.query(Document).filter(Document.id==document_id).first()
    return documnet

@router.delete("/documents/{document_id}")
def delete_document(document_id:int,db:Session=Depends(get_db)):
    document=db.query(Document).filter(Document.id==document_id).first()
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    db.delete(document)
    db.commit()
    return {
        "message":f"Document {document_id} deleted"
    }
