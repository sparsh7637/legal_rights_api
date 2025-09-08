
# 🏛 Women Empowerment RAG Microservice API

This project is a **microservice-based Retrieval-Augmented Generation (RAG) API** built with **FastAPI**, **LangChain**, **Qdrant Cloud**, and **Hugging Face-hosted models**.
It answers queries related to **Safety and Legal Rights for Women Empowerment (India focus)** by retrieving relevant documents and generating context-grounded answers.

---

## 🌐 Live API

The microservice is deployed and publicly available at:

**Base URL:**
👉 [https://legal-rag-api-oe37.onrender.com/](https://legal-rag-api-oe37.onrender.com/)



This is the **API endpoint** you will call from clients (mobile apps, chatbots, or web apps).

---

## 🚀 Features

* **Hosted Hugging Face models**

  * LLM: `openai/gpt-oss-20b`
  * Embeddings: `sentence-transformers/all-MiniLM-L6-v2`

* **Qdrant Cloud Vector Database**

  * Stores document embeddings for women’s rights and safety.
  * Fast semantic + keyword retrieval.

* **Ensemble Retrieval**

  * Combines **semantic retrieval (Qdrant)** and **keyword retrieval (BM25)**.
  * Weighted blend for best accuracy.

* **REST API with FastAPI**

  * `/health` → check service status.
  * `/rag` → submit a query, get a contextual answer.

---

## 📂 Project Structure

```
app/
 ├─ main.py                  # FastAPI app & endpoints
 ├─ config.py                # Environment variables & settings
 ├─ models/
 │   └─ llm_loader.py        # Hugging Face hosted LLM loader
 ├─ rag/
 │   ├─ embeddings.py        # Hosted embeddings client
 │   ├─ loader.py            # JSON → LangChain Documents
 │   ├─ qdrant_utils.py      # Ensures Qdrant collections
 │   ├─ ingest.py            # One-time document ingestion
 │   ├─ pipeline.py          # Builds retrievers & RAG chain
 │   ├─ prompts.py           # Prompt templates
 │   └─ utils.py             # Helper functions
```

---

## ⚙️ Setup (Local)

### 1. Clone & create venv

```bash
git clone https://github.com/<your-org>/<repo>.git
cd <repo>
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Install requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure `.env`

```ini
HUGGINGFACEHUB_API_TOKEN=hf_xxx
HF_LLM_REPO=openai/gpt-oss-20b
HF_EMBEDDING_REPO=sentence-transformers/all-MiniLM-L6-v2

QDRANT_URL=https://<cluster-id>.qdrant.io
QDRANT_API_KEY=your_qdrant_key
QDRANT_COLLECTION=women_rights_rag

CORS_ORIGINS=*
```

### 4. Ingest documents

```bash
python -m app.rag.ingest
```

### 5. Run API

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

---

## 📡 API Usage

### 1. `GET /health`

Check if API is alive.

**Request**

```bash
curl https://legal-rag-api-oe37.onrender.com/health
```

**Response**

```json
{"status":"ok"}
```

---

### 2. `POST /rag`

Submit a natural language query.
**URL:**

```
https://legal-rag-api-oe37.onrender.com/rag
```

**Headers**

```http
Content-Type: application/json
```

**Request Body**

```json
{
  "query": "Does the POSH Act require an Internal Complaints Committee?"
}
```

**Response**

```json
{
  "response": "Yes. The POSH Act mandates organizations with 10 or more employees to form an Internal Complaints Committee (ICC) to handle sexual harassment complaints."
}
```

---

## 🧪 More Sample Queries

```json
{"query": "Can a woman stay in the shared household under the Domestic Violence Act?"}
{"query": "What is the time limit for filing a sexual harassment complaint under the POSH Act?"}
{"query": "What legal protections exist for women at work and home?"}
```

---

## 🛡 Safety Mechanisms

* **Grounded responses** → answers only from ingested documents.
* **Fallback** → if no relevant info, responds with:
  *“I don’t have enough information in the provided documents.”*
* **Disclaimer** → responses are informational only, not legal advice.



