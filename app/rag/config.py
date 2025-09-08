from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Tokens (HF token can come via either name)
    HUGGINGFACEHUB_API_TOKEN: str = Field(default="", alias="HF_TOKEN")

    # Qdrant Cloud (managed)
    QDRANT_URL: str = ""
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION: str = "women_rights_rag"

    # Hosted models on Hugging Face
    HF_LLM_REPO: str = "openai/gpt-oss-20b"
    HF_EMBEDDING_REPO: str = "sentence-transformers/all-MiniLM-L6-v2"

    # CORS
    CORS_ORIGINS: str = "*"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow" 

settings = Settings()
