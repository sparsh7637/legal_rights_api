from typing import List
from langchain.schema import Document

def clean_text(text: str) -> str:
    text = (text or "").replace("\u00a0", " ").strip()
    return " ".join(text.split())

def flatten_json_records(records: list[dict], source_name: str) -> List[Document]:
    docs: List[Document] = []
    for rec in records:
        title = rec.get("title", "")
        sections = rec.get("sections", [])
        for sec in sections:
            chunk = f"{title} — {sec.get('heading','')}\n{sec.get('text','')}"
            docs.append(
                Document(
                    page_content=clean_text(chunk),
                    metadata={
                        "source": source_name,
                        "title": title,
                        "heading": sec.get("heading", ""),
                        "jurisdiction": rec.get("jurisdiction", ""),
                        "year": rec.get("year", ""),
                    },
                )
            )
    return docs
