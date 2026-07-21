from fastapi import APIRouter, HTTPException
from utils.logger import logger

from services.rag_service import RAGService

from models.request_model import (
    RAGRequest
)

from models.response_model import (
    RAGResponse
)

router = APIRouter(
    prefix="/rag",
    tags=["Healthcare RAG Copilot"]
)

service = RAGService()


@router.post(
    "/ask",
    response_model=RAGResponse,
    summary="Ask Healthcare RAG Question"
)
async def ask_question(
    request: RAGRequest
):

    try:

        logger.info(
            f"RAG Request Received: "
            f"{request.question}"
        )

        response = await service.ask_question(
            request
        )

        logger.success(
            "RAG Request Processed Successfully"
        )

        return response

    except Exception as ex:

        logger.exception(
            f"RAG Request Failed: {str(ex)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )


@router.get(
    "/health",
    summary="Application Health Check"
)
async def health_check():

    try:

        logger.info(
            "Health Check Endpoint Invoked"
        )

        response = await service.health_check()

        logger.success(
            "Health Check Completed"
        )

        return response

    except Exception as ex:

        logger.exception(
            f"Health Check Failed: {str(ex)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )


@router.get(
    "/stats",
    summary="Knowledge Base Statistics"
)
async def get_collection_stats():

    try:

        logger.info(
            "Collection Statistics Requested"
        )

        response = (
            await service.get_collection_stats()
        )

        logger.success(
            "Collection Statistics Retrieved"
        )

        return response

    except Exception as ex:

        logger.exception(
            f"Statistics Retrieval Failed: "
            f"{str(ex)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )


@router.post(
    "/reset",
    summary="Reset Knowledge Base"
)
async def reset_knowledge_base():

    try:

        logger.warning(
            "Knowledge Base Reset Requested"
        )

        response = (
            await service.reset_knowledge_base()
        )

        logger.success(
            "Knowledge Base Reset Completed"
        )

        return response

    except Exception as ex:

        logger.exception(
            f"Knowledge Base Reset Failed: "
            f"{str(ex)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )