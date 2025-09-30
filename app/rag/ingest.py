# app/rag/ingest.py
from pathlib import Path
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant as QdrantVS
from dotenv import load_dotenv
from app.rag.config import settings
from app.rag.embeddings import get_embeddings
from app.rag.loader import load_json_docs
from app.rag.qdrant_utils import ensure_collection

def build_vector_store(reset: bool = True):
    load_dotenv()
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        prefer_grpc=False,
    )
    embeddings = get_embeddings()

    # Ensure collection exists (optionally wipe if reset)
    ensure_collection(client, embeddings, reset=True)

    # Upsert documents
    docs = load_json_docs()
    _ = QdrantVS.from_documents(
        docs,
        embeddings,
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        collection_name=settings.QDRANT_COLLECTION,
    )
    print(f"Upserted {len(docs)} docs to Qdrant collection '{settings.QDRANT_COLLECTION}'")

if __name__ == "__main__":
    print("Building Qdrant index (hosted embeddings)...")
    build_vector_store(reset=True)
    print("Done.")
