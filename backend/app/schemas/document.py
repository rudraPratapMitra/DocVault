from pydantic import BaseModel,ConfigDict

class DocumentResponse(BaseModel):
    id: int
    filename: str
    status: str
    model_config = ConfigDict(
        from_attributes=True
    )