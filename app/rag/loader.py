# app/rag/loader.py
import json
from pathlib import Path
from typing import List
from langchain.schema import Document
from app.rag.utils import flatten_json_records

DATA_DIR = Path(__file__).parent / "data"

def load_json_docs() -> List[Document]:
    docs: List[Document] = []
    for p in DATA_DIR.glob("*.json"):
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        records = data if isinstance(data, list) else [data]
        docs.extend(flatten_json_records(records, source_name=p.name))
    return docs
