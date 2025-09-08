# app/rag/pipeline.py
from typing import List
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant as QdrantVS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers.ensemble import EnsembleRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from app.rag.config import settings
from app.rag.prompts import build_prompt
from app.models.llm_loader import load_llm
from app.rag.loader import load_json_docs
from app.rag.embeddings import get_embeddings
from app.rag.qdrant_utils import ensure_collection

def _qdrant_vectorstore() -> QdrantVS:
    embeddings = get_embeddings()
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        prefer_grpc=False,
    )
    ensure_collection(client, embeddings, reset=False)

    return QdrantVS(
        client=client,
        collection_name=settings.QDRANT_COLLECTION,
        embeddings=embeddings,
    )

def _build_vector_retriever():
    vs = _qdrant_vectorstore()
    return vs.as_retriever(search_kwargs={"k": 6})

def _build_bm25_retriever() -> BM25Retriever:
    raw_docs: List[Document] = load_json_docs()
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)
    split_docs = splitter.split_documents(raw_docs)
    retriever = BM25Retriever.from_documents(split_docs)
    retriever.k = 6
    return retriever

def build_ensemble_retriever():
    vec = _build_vector_retriever()
    bm25 = _build_bm25_retriever()
    return EnsembleRetriever(
        retrievers=[vec, bm25],
        weights=[0.65, 0.35],
    )

def build_rag_chain():
    retriever = build_ensemble_retriever()
    prompt = build_prompt()
    llm = load_llm()
    parser = StrOutputParser()

    def join_context(docs: List[Document]) -> str:
        return "\n\n".join([d.page_content for d in docs])

    chain = (
        {"context": retriever | join_context, "question": RunnablePassthrough()}
        | prompt
        | llm
        | parser
    )
    return chain
