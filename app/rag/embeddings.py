# app/rag/embeddings.py
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from app.rag.config import settings

def get_embeddings():
    """
    Hosted embeddings via HF Inference API (no local model download).
    Requires HUGGINGFACEHUB_API_TOKEN / HF_TOKEN in the environment.
    """

    return HuggingFaceEndpointEmbeddings(
        repo_id=settings.HF_EMBEDDING_REPO,   # e.g., "sentence-transformers/all-MiniLM-L6-v2"
        task="feature-extraction",
        huggingfacehub_api_token=settings.HUGGINGFACEHUB_API_TOKEN or None,
    )
