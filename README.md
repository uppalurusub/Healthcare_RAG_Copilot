# 🏥 Healthcare RAG Copilot

An Enterprise AI-powered **Healthcare Retrieval-Augmented Generation (RAG) Copilot** built using **FastAPI**, **AutoGen Multi-Agent Framework**, **ChromaDB**, **React TypeScript**, and **Streamlit**.

The system enables healthcare professionals to ask clinical questions and receive accurate, context-aware responses by retrieving information from medical guidelines, protocols, and SOP documents.

---

# 🚀 Features

- 🤖 AutoGen 0.7.5 Multi-Agent Collaboration
- 📚 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic Search using ChromaDB
- 🩺 Clinical Guideline Retrieval
- 📑 SOP Document Retrieval
- 📋 Clinical Protocol Search
- 🧠 LLM-powered Healthcare Assistant
- ⚡ FastAPI REST API
- 🎨 React TypeScript Frontend
- 📈 Streamlit Dashboard
- 📦 Modular Enterprise Architecture
- 📝 Comprehensive Logging
- 🔒 Production Ready API Design

---

# System Architecture

```
                    +----------------------+
                    |   React Frontend     |
                    +----------+-----------+
                               |
                               |
                    REST API (FastAPI)
                               |
              +----------------+----------------+
              |                                 |
      RAG Service Layer                 Health APIs
              |
              |
      AutoGen Multi-Agent System
              |
   +----------+-----------+
   |                      |
Retriever Agent     Validation Agent
   |                      |
   +----------+-----------+
              |
        ChromaDB Vector Store
              |
    Sentence Transformer Embeddings
              |
     PDF Knowledge Base
       • Clinical Guidelines
       • SOPs
       • Protocols
```

---

# Project Structure

```
Healthcare_RAG_Copilot/
│
├── backend/
│   └── healthcare-rag-copilot-python-app/
│       ├── agents/
│       ├── config/
│       ├── implementation/
│       ├── knowledge_base/
│       │     ├── clinical_guidelines/
│       │     ├── protocols/
│       │     └── sops/
│       ├── chroma_db/
│       ├── models/
│       ├── routers/
│       ├── services/
│       ├── utils/
│       ├── main.py
│       └── logs/
│
├── ui/
│   ├── reactjs/
│   │      └── healthcare-rag-copilot-reactjs-app/
│   └── streamlit/
│          └── healthcare-rag-copilot-streamlit-app/
│
├── requirements.txt
└── README.md
```

---

# Technology Stack

## Backend

- Python
- FastAPI
- AutoGen 0.7.5
- ChromaDB
- Sentence Transformers
- OpenAI
- Uvicorn
- Loguru
- MLflow
- PyPDF

---

## Frontend

- React 19
- TypeScript
- Vite
- Axios
- React Markdown
- Lucide Icons

---

## Vector Database

- ChromaDB

---

## AI Components

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Embeddings
- Multi-Agent Collaboration

---

# Knowledge Sources

The project includes healthcare documents such as:

## Clinical Guidelines

- Diabetes Management
- Hypertension
- Heart Failure
- COPD
- Asthma
- Chronic Kidney Disease
- Stroke
- Sepsis
- Obesity
- Depression

---

## Clinical Protocols

- Cardiology
- ICU Management
- COVID Treatment
- Oncology Trial
- Diabetes Protocol
- Surgery
- Vaccination

---

## SOP Documents

- Clinical Documentation
- Adverse Event Reporting
- Additional Healthcare SOPs

---

# Backend Installation

## Clone Repository

```bash
git clone https://github.com/your-org/Healthcare_RAG_Copilot.git

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

Linux / Mac

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the backend.

Example:

```env
OPENAI_API_KEY=your_openai_key
MODEL_NAME=gpt-4
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_DB_PATH=./chroma_db
```

---

# Run Backend

```bash
cd backend/healthcare-rag-copilot-python-app

uvicorn main:app --reload
```

Server

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

# Frontend Installation

Navigate to the React project.

```bash
cd ui/reactjs/healthcare-rag-copilot-reactjs-app
```

Install packages

```bash
npm install
```

Run

```bash
npm run dev
```

Application

```
http://localhost:5173
```

---

# Streamlit Application

Navigate to

```bash
cd ui/streamlit/healthcare-rag-copilot-streamlit-app
```

Install

```bash
pip install -r requirements.txt
```

Run

```bash
streamlit run app.py
```

---

# REST API

## Ask Question

**POST**

```
/rag/ask
```

### Request

```json
{
  "question": "What is the recommended treatment for hypertension?"
}
```

---

### Response

```json
{
  "answer": "The recommended treatment includes...",
  "sources": [
    "hypertension_guideline.pdf"
  ]
}
```

---

## Health Check

```
GET /rag/health
```

---

## Application Status

```
GET /
```

---

## Readiness Probe

```
GET /ready
```

---

## Liveness Probe

```
GET /live
```

---

# Multi-Agent Workflow

```
User Question
      │
      ▼
Retriever Agent
      │
Retrieve Relevant Chunks
      │
      ▼
Validation Agent
      │
Context Verification
      │
      ▼
LLM Response Generation
      │
      ▼
Final Healthcare Answer
```

---

# Logging

The application automatically creates log files.

```
logs/

healthcare_rag.log

healthcare_rag_error.log
```

---

# Vector Database

The application stores embeddings using ChromaDB.

```
chroma_db/
```

Documents are indexed for semantic retrieval.

---

# Security Recommendations

- Store API keys in environment variables.
- Restrict CORS in production.
- Secure APIs using OAuth2 or JWT.
- Encrypt sensitive healthcare data.
- Implement role-based access control (RBAC).

---

# Future Enhancements

- Hybrid Search (BM25 + Vector Search)
- Multiple LLM Support
- LangGraph Integration
- Azure OpenAI Support
- Medical Citation Generation
- Clinical Decision Support
- Conversation Memory
- Feedback-based Learning
- Document Upload Portal
- Multi-language Support

---

# Performance Optimization

- Embedding Cache
- Async FastAPI APIs
- Batch Vector Search
- Incremental Document Indexing
- Response Streaming
- GPU Embedding Support

---

# License

This project is intended for educational and enterprise healthcare AI development purposes.

---

# Author

Healthcare RAG Copilot

Enterprise AI Solution for Clinical Knowledge Retrieval using FastAPI, AutoGen, ChromaDB, and React TypeScript.