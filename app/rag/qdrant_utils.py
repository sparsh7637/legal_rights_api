# app/rag/qdrant_utils.py
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, OptimizersConfigDiff
from app.rag.config import settings

def ensure_collection(client: QdrantClient, embeddings, reset: bool = False) -> None:
    """
    Create or recreate a Qdrant collection. We infer vector size by embedding a tiny sample.
    """
    name = settings.QDRANT_COLLECTION

    if reset:
        try:
            client.delete_collection(name)
        except Exception:
            pass

    # infer vector size once
    test_vec = embeddings.embed_query("hello")
    vector_size = len(test_vec)

    # create if missing
    collections = [c.name for c in client.get_collections().collections]
    if name not in collections:
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            optimizers_config=OptimizersConfigDiff(memmap_threshold=20000),
        )
