# app/rag/loader.py
import json
from pathlib import Path
from typing import List, Union
from langchain.schema import Document

DATA_DIR = Path(__file__).parent / "data"

def flatten_json_records(records: Union[List, dict], source_name: str) -> List[Document]:
    """
    Convert JSON records into LangChain Document objects.
    Each record is stringified to ensure valid page_content.
    """
    docs: List[Document] = []
    if isinstance(records, dict):
        records = [records]

    for r in records:
        # Convert dicts/lists to JSON string, else cast to str
        if isinstance(r, (dict, list)):
            text = json.dumps(r, ensure_ascii=False, indent=None)
        else:
            text = str(r).strip()

        if not text:
            continue  # skip empty records

        docs.append(
            Document(
                page_content=text,
                metadata={"source": source_name}
            )
        )

    return docs


def load_json_docs() -> List[Document]:
    """
    Load the first JSON file found in the `data` directory
    and return as a list of Documents.
    """
    docs: List[Document] = []
    json_files = list(DATA_DIR.glob("*.json"))

    if not json_files:
        print("[Loader] No JSON files found in data/ folder.")
        return docs

    p = json_files[0]
    print(f"[Loader] Loading data from: {p}")

    with open(p, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[Loader] JSON decode error in {p}: {e}")
            return docs

    records = data if isinstance(data, list) else [data]
    docs = flatten_json_records(records, source_name=p.name)

    print(f"[Loader] Loaded {len(docs)} documents from {p.name}")
    return docs
