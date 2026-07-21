# 🏥 Healthcare RAG Copilot

## Overview

Healthcare RAG Copilot is an Enterprise Retrieval-Augmented Generation (RAG) application designed to answer healthcare-related questions using trusted medical documents instead of relying solely on Large Language Models.

The application combines:

- AutoGen Multi-Agent Architecture
- ChromaDB Vector Database
- Retrieval-Augmented Generation (RAG)
- FastAPI REST APIs
- MLflow Tracking
- Loguru Logging

to provide evidence-based clinical responses with document citations and validation.

---

# Features

- Enterprise Healthcare Knowledge Assistant
- Retrieval-Augmented Generation (RAG)
- AutoGen 0.7.5 Multi-Agent Collaboration
- Clinical Guideline Search
- SOP Search
- Hospital Protocol Search
- Vector Similarity Search using ChromaDB
- Evidence-Based Answers
- Source Attribution
- Clinical Validation Agent
- Conversation History Support
- MLflow Experiment Tracking
- Structured Logging using Loguru
- FastAPI REST API

---

# Architecture

```
                    User Question
                          │
                          ▼
                  FastAPI REST API
                          │
                          ▼
                   Router Layer
                          │
                          ▼
                  Service Layer
                          │
                          ▼
              RAG Implementation Layer
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
 Vector Store      AutoGen Agents      MLflow Logging
        │                 │
        ▼                 ▼
   ChromaDB        Multi-Agent Reasoning
        │
        ▼
 Clinical Guidelines
 SOP Documents
 Protocol Documents
```

---

# AutoGen Multi-Agent Workflow

The application uses three specialized AutoGen agents.

## 1. Retrieval Agent

Responsibilities

- Analyze retrieved documents
- Extract relevant information
- Identify supporting evidence
- Summarize retrieved content

---

## 2. Medical Knowledge Agent

Responsibilities

- Interpret clinical guidelines
- Analyze SOPs
- Analyze protocols
- Generate evidence-based responses
- Avoid hallucinations

---

## 3. Validation Agent

Responsibilities

- Validate medical facts
- Verify protocol compliance
- Detect unsupported claims
- Assign confidence scores

---

# Technology Stack

| Component | Technology |
|------------|------------|
| Backend | FastAPI |
| Agent Framework | AutoGen 0.7.5 |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| PDF Processing | PyPDF |
| Experiment Tracking | MLflow |
| Logging | Loguru |
| Language Model | OpenAI Compatible API |
| Validation | Pydantic |

---

# Project Structure

```
Healthcare_RAG_Copilot/

│
├── app/
│   ├── agents/
│   │      rag_agents.py
│   │
│   ├── config/
│   │      llm_config.py
│   │      llm_models_config.py
│   │
│   ├── implementation/
│   │      rag_impl.py
│   │
│   ├── memory/
│   │      vector_store.py
│   │
│   ├── models/
│   │      request_model.py
│   │      response_model.py
│   │
│   ├── routers/
│   │      rag_router.py
│   │
│   ├── services/
│   │      rag_service.py
│   │
│   ├── utils/
│   │      document_loader.py
│   │      ingest_documents.py
│   │      prompt_templates.py
│   │      logger.py
│   │
│   └── main.py
│
├── chroma_db/
│
├── knowledge_base/
│      clinical_guidelines/
│      protocols/
│      sop/
│
├── logs/
│
├── requirements.txt
└── ask_requests.json
```

---

# Knowledge Base

The application indexes healthcare documents including:

## Clinical Guidelines

- Hypertension
- Diabetes
- COPD
- Asthma
- Heart Failure
- Chronic Kidney Disease
- Stroke
- Sepsis
- Obesity
- Depression

---

## Protocols

- Cardiology Protocol
- COVID Treatment Protocol
- Diabetes Clinical Protocol
- and more...

---

## SOP Documents

Healthcare operational procedures.

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd Healthcare_RAG_Copilot
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Environment

Create a `.env`

Example

```env
OPENAI_API_KEY=your_api_key

OPENAI_BASE_URL=https://your-provider.com/v1

MODEL_NAME=gpt-4o-mini
```

---

# Run Application

Ingest Documents into chromadb using below command
```bash
python -m utils.ingest_documents
```

```bash
uvicorn app.main:app --reload
```

Application

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# REST APIs

## Home

```
GET /
```

---

## Readiness

```
GET /ready
```

---

## Liveness

```
GET /live
```

---

## Ask Healthcare Question

```
POST /rag/ask
```

### Sample Request

```json
{
  "question": "What is the first-line treatment for hypertension?",
  "top_k": 5,
  "document_types": [
    "guideline"
  ],
  "departments": [
    "cardiology"
  ],
  "include_sources": true,
  "conversation_history": []
}
```

---

### Sample Response

```json
{
  "success": true,
  "question": "What is the first-line treatment for hypertension?",
  "answer": "ACE inhibitors, ARBs, calcium channel blockers, or thiazide diuretics are recommended as first-line therapy depending on patient characteristics.",
  "validation": {
    "is_valid": true,
    "confidence_score": 0.97,
    "validation_notes": "Validated using hypertension guideline."
  },
  "retrieval_metadata": {
    "retrieved_documents": 5,
    "top_k": 5,
    "retrieval_time_seconds": 0.42
  },
  "sources": [
    {
      "document": "hypertension_guideline.pdf",
      "page": 12
    }
  ],
  "execution_time_seconds": 2.4,
  "message": "Success"
}
```

---

## Health Check

```
GET /rag/health
```

Returns

- Agent status
- Vector database status
- Application status

---

## Collection Statistics

```
GET /rag/stats
```

Returns

- Indexed documents
- Collections
- Vector counts

---

## Reset Knowledge Base

```
POST /rag/reset
```

Rebuilds or resets the vector store.

---

# Logging

Loguru generates

```
logs/

healthcare_rag.log

healthcare_rag_error.log
```

Features

- Console logging
- File logging
- Error logging
- Rotation
- Compression
- Retention

---

# MLflow Tracking

Every RAG request is tracked.

Logged Information

- Question
- Retrieved documents
- Generated response
- Endpoint
- Source
- Execution metadata

Start MLflow

```bash
mlflow server \
--backend-store-uri sqlite:///mlflow.db \
--default-artifact-root ./mlruns \
--host 0.0.0.0 \
--port 5000
```

Open

```
http://localhost:5000
```

---

# RAG Workflow

```
User Question
      │
      ▼
Embedding Generation
      │
      ▼
ChromaDB Similarity Search
      │
      ▼
Retrieve Top-K Documents
      │
      ▼
Retrieval Agent
      │
      ▼
Medical Knowledge Agent
      │
      ▼
Validation Agent
      │
      ▼
Evidence-Based Response
      │
      ▼
Return Sources + Confidence Score
```

---

# Advantages

- Minimizes hallucinations
- Uses trusted healthcare documents
- Explainable AI responses
- Source citations
- Multi-agent reasoning
- Scalable architecture
- Modular codebase
- Production-ready logging
- Experiment tracking

---

# Future Enhancements

- Hybrid Search (BM25 + Vector Search)
- Reranking Models
- FHIR Integration
- HL7 Support
- Patient-specific Retrieval
- Role-Based Access Control (RBAC)
- Streaming Responses
- OCR for scanned PDFs
- Multilingual Support
- Knowledge Base Versioning

---

# Author

Enterprise Healthcare AI Solution

Built using

- FastAPI
- AutoGen 0.7.5
- ChromaDB
- MLflow
- Loguru
- Retrieval-Augmented Generation (RAG)