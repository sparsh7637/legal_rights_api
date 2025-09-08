

# 🏛 Women Empowerment RAG Microservice API

This project is a **microservice-based Retrieval-Augmented Generation (RAG) API** built with **FastAPI**, **LangChain**, **Qdrant Cloud**, and **Hugging Face-hosted models**.
It enables answering user queries about **Safety and Legal Rights for Women Empowerment** by retrieving relevant legal/policy documents and generating contextual answers.

---

## 🚀 Features

* **Hosted Hugging Face models**

  * LLM: `openai/gpt-oss-20b` (text generation)
  * Embeddings: `sentence-transformers/all-MiniLM-L6-v2` (feature extraction)

* **Qdrant Cloud Vector Database**

  * Stores embeddings of women’s legal rights documents.
  * Enables semantic + keyword-based hybrid retrieval.

* **Ensemble Retrieval**

  * **Dense retriever (Qdrant)** for semantic matches.
  * **BM25 retriever** for keyword exact matches.
  * **Weighted combination** for best results.

* **REST API with FastAPI**

  * `/health` – service health check.
  * `/rag` – query endpoint, returns context-grounded answers.

---

## 📂 Project Structure

```
app/
 ├─ main.py                  # FastAPI entrypoint
 ├─ config.py                # Environment configuration
 ├─ models/
 │   └─ llm_loader.py        # Loads HuggingFace-hosted LLM
 ├─ rag/
 │   ├─ embeddings.py        # Hosted embeddings client
 │   ├─ loader.py            # Loads JSON docs into LangChain Documents
 │   ├─ qdrant_utils.py      # Ensures Qdrant collections exist
 │   ├─ ingest.py            # One-time ingestion to Qdrant
 │   ├─ pipeline.py          # Builds retrievers & RAG chain
 │   ├─ prompts.py           # Prompt templates for QA
 │   └─ utils.py             # JSON/document flattening helpers
 └─ ...
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/<your-org>/<repo-name>.git
cd <repo-name>
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment

Create `.env` file:

```ini
# Hugging Face
HUGGINGFACEHUB_API_TOKEN=hf_xxx
HF_LLM_REPO=openai/gpt-oss-20b
HF_EMBEDDING_REPO=sentence-transformers/all-MiniLM-L6-v2

# Qdrant Cloud
QDRANT_URL=https://<cluster-id>.qdrant.io
QDRANT_API_KEY=your_qdrant_key
QDRANT_COLLECTION=women_rights_rag

# API
CORS_ORIGINS=*
```

---

## 🏗️ Workflow

### 1. Ingest documents (one-time or when adding data)

```bash
python -m app.rag.ingest
```

This:

* Loads JSON legal/policy docs from `app/rag/data/`.
* Embeds text via Hugging Face hosted embedding model.
* Stores vectors into Qdrant Cloud under the configured collection.

### 2. Run API locally

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

API docs auto-generated at:

* Swagger UI: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
* ReDoc: [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)

---

## 📡 API Usage

### `GET /health`

Check service status.

```bash
curl http://127.0.0.1:8080/health
```

**Response**

```json
{"status":"ok"}
```

---

### `POST /rag`

Submit a query.
Request body:

```json
{
  "query": "Does the POSH Act require an Internal Complaints Committee?"
}
```

Response:

```json
{
  "response": "Yes. The POSH Act mandates that organizations with 10 or more employees must form an Internal Complaints Committee (ICC) to handle sexual harassment complaints."
}
```

Another example:

```json
{
  "query": "Can a woman stay in her shared household under the Domestic Violence Act?"
}
```

Response:

```json
{
  "response": "Yes. Under the Protection of Women from Domestic Violence Act (PWDVA), a woman has the right to reside in the shared household, regardless of ownership or title."
}
```

---

## 🛡 Safety & Ethics

* **Grounded responses**: The RAG pipeline only answers from ingested context.
* **Fallback**: If context is missing, it replies with:
  *“I don’t have enough information in the provided documents.”*
* **Disclaimers**: This system is **informational only** and **not a substitute for legal advice**.
