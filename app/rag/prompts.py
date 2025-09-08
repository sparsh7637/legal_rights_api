# app/rag/prompts.py
from langchain_core.prompts import ChatPromptTemplate

SYSTEM = """You are a careful assistant that answers only from the provided context.
Topic: Safety and Legal Rights for Women Empowerment (India focus).
If the answer is not in the context, say you don't have enough information.
Be clear, concise, and practical.
"""

USER = """Question:
{question}

Context:
{context}

Instructions:
- Use only the context.
- If unsure, say: "I don't have enough information in the provided documents."
- Keep the answer concise and actionable.
"""

def build_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM),
        ("user", USER),
    ])
