from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Document(Base):
    __tablename__="documents"

    id=Column(Integer,primary_key=True,index=True)
    filename=Column(String,nullable=False)
    status=Column(String,default="uploaded")
    created_at=Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    owner_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    file_path=Column(String,nullable=False)
    content_type=Column(String,nullable=False)
    file_size=Column(Integer,nullable=False)