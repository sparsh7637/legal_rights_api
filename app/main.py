from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, constr

from app.rag.pipeline import build_rag_chain
from app.rag.config import settings

app = FastAPI(title="Women Empowerment RAG API (Qdrant Cloud)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RAGRequest(BaseModel):
    query: constr(strip_whitespace=True, min_length=3) = Field(..., description="User query")

class RAGResponse(BaseModel):
    response: str

@app.get("/health")
def health():
    return {"status": "ok"}

rag_chain = build_rag_chain()

@app.post("/rag", response_model=RAGResponse)
def rag_endpoint(payload: RAGRequest):
    try:
        answer = rag_chain.invoke(payload.query).strip()
        return RAGResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG error: {e}")
