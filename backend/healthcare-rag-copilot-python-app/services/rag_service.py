from utils.logger import logger

from implementation.rag_impl import (
    RAGImplementation
)

from models.request_model import (
    RAGRequest
)

from models.response_model import (
    RAGResponse
)

import mlflow
from datetime import datetime

mlflow.set_tracking_uri(
    "http://localhost:5000"
)

mlflow.set_experiment(
    "Healthcare_RAG_Copilot_Interface"
)

class RAGService:

    def __init__(self):

        logger.info(
            "Initializing Healthcare RAG Service"
        )

        self.impl = RAGImplementation()

        logger.success(
            "Healthcare RAG Service Initialized"
        )

    async def ask_question(
        self,
        request: RAGRequest
    ) -> RAGResponse:

        try:

            logger.info(
                f"Question Received: {request.question}"
            )

            
            with mlflow.start_run(
                run_name=
                f"Healthcare_RAG_Copilot_Ask_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            ):
                mlflow.log_param(
                    "input_text",
                    request
                )

                response = await self.impl.ask_question(

                    question=request.question,

                    top_k=request.top_k,

                    document_types=request.document_types,

                    departments=request.departments,

                    include_sources=request.include_sources
                )

                mlflow.log_param(
                    "response",
                    response
                )

                mlflow.set_tag(
                    "source",
                    "FastAPI"
                )

                mlflow.set_tag(
                    "endpoint",
                    "rag/ask"
                )

            logger.success(
                "Healthcare RAG Request Completed"
            )

            return response

        except Exception as ex:

            logger.exception(
                f"Healthcare RAG Service Failed: {str(ex)}"
            )

            return RAGResponse(

                success=False,

                question=request.question,

                answer="",

                validation={
                    "is_valid": False,
                    "confidence_score": 0.0,
                    "validation_notes": str(ex)
                },

                retrieval_metadata={
                    "retrieved_documents": 0,
                    "top_k": request.top_k,
                    "retrieval_time_seconds": 0.0
                },

                sources=[],

                agent_outputs=[],

                execution_time_seconds=0.0,

                message=f"Service Error: {str(ex)}"
            )

    async def health_check(self) -> dict:

        try:

            logger.info(
                "Performing RAG Service Health Check"
            )

            vector_stats = (
                self.impl.vector_store
                .get_collection_stats()
            )

            agent_status = (
                self.impl.agents
                .get_agent_status()
            )

            logger.success(
                "Health Check Completed"
            )

            return {

                "status": "healthy",

                "vector_store": vector_stats,

                "agents": agent_status
            }

        except Exception as ex:

            logger.exception(
                f"Health Check Failed: {str(ex)}"
            )

            return {

                "status": "unhealthy",

                "error": str(ex)
            }

    async def get_collection_stats(
        self
    ) -> dict:

        try:

            logger.info(
                "Fetching Collection Statistics"
            )

            stats = (
                self.impl.vector_store
                .get_collection_stats()
            )

            logger.success(
                "Collection Statistics Retrieved"
            )

            return stats

        except Exception as ex:

            logger.exception(
                f"Failed to Fetch Collection Stats: {str(ex)}"
            )

            return {
                "success": False,
                "message": str(ex)
            }

    async def reset_knowledge_base(
        self
    ) -> dict:

        try:

            logger.warning(
                "Resetting Knowledge Base"
            )

            result = (
                self.impl.vector_store
                .reset_collection()
            )

            logger.success(
                "Knowledge Base Reset Completed"
            )

            return result

        except Exception as ex:

            logger.exception(
                f"Reset Failed: {str(ex)}"
            )

            return {
                "success": False,
                "message": str(ex)
            }