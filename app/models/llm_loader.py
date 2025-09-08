from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from app.rag.config import settings

def load_llm():
    load_dotenv()
    llm = HuggingFaceEndpoint(
        repo_id=settings.HF_LLM_REPO,
        task="text-generation",
        max_new_tokens=512,
        temperature=0.2,
        top_p=0.95,
        repetition_penalty=1.05,
        return_full_text=False,
    )
    return ChatHuggingFace(llm=llm)
