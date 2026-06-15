from sqlalchemy import text
from app.core.database import engine
from app.api.documents import router as document_router
from app.api.user import router as user_router
from fastapi import FastAPI


app=FastAPI()

app.include_router(document_router)
app.include_router(user_router)

@app.get("/")
def home():
    return{
        "message":"DocValut Running"
    }

@app.get("/health")
def health():
    return{
        "status":"healthy"
    }

@app.get("/db-test")
def db_test():

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return {"status": "connected"}