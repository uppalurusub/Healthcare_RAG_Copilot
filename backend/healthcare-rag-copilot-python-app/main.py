import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.logger import logger

from routers.rag_router import router as rag_router


# =====================================================
# Loguru Configuration
# =====================================================

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<cyan>{name}</cyan>:"
        "<cyan>{function}</cyan>:"
        "<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
)

logger.add(
    f"{LOG_DIR}/healthcare_rag.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="INFO",
    enqueue=True
)

logger.add(
    f"{LOG_DIR}/healthcare_rag_error.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="ERROR",
    enqueue=True
)


# =====================================================
# FastAPI App
# =====================================================

app = FastAPI(
    title="Healthcare RAG Copilot",
    description="""
    Enterprise Healthcare RAG System

    Features:
    - AutoGen 0.7.5 Multi-Agent Collaboration
    - ChromaDB Vector Search
    - Clinical Guidelines Retrieval
    - SOP Retrieval
    - Protocol Search
    - Validation Agent
    - Healthcare Knowledge Assistant
    """,
    version="1.0.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =====================================================
# Register Routers
# =====================================================

app.include_router(rag_router)




# =====================================================
# Root Endpoint
# =====================================================

@app.get(
    "/",
    tags=["Application"]
)
async def home():

    logger.info(
        "Home Endpoint Accessed"
    )

    return {

        "application":
            "Healthcare RAG Copilot",

        "version":
            "1.0.0",

        "framework":
            "FastAPI",

        "autogen_version":
            "0.7.5",

        "status":
            "running"
    }


# =====================================================
# Readiness Probe
# =====================================================

@app.get(
    "/ready",
    tags=["Application"]
)
async def readiness_check():

    return {
        "status": "ready"
    }


# =====================================================
# Liveness Probe
# =====================================================

@app.get(
    "/live",
    tags=["Application"]
)
async def liveness_check():

    return {
        "status": "alive"
    }


