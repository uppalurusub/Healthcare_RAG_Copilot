from datetime import datetime
import time



from app.config.settings import (
    settings,
    usage_capture,
    INPUT_PRICE_PER_1M,
    OUTPUT_PRICE_PER_1M,
)
logger = settings.get_logger()

from app.implementation.rag_impl import (
    RAGImplementation
)

from app.schemas.request_model import (
    RAGRequest
)

from app.schemas.response_model import (
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

            start_time = datetime.now()
            start_ts = time.perf_counter()

            logger.info(
                f"Question Received: {request.question}"
            )

            
            with mlflow.start_run(
                run_name=
                f"Healthcare_RAG_Copilot_Ask_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            ):
                mlflow.log_param("start_time", start_time.isoformat())
                mlflow.set_tag("source", "FastAPI")
                mlflow.set_tag("endpoint", "monitoring/analyze")
                mlflow.set_tag("llm_provider", "OpenRouter")

                with usage_capture() as usage:

                    response = await self.impl.ask_question(

                        question=request.question,

                        top_k=request.top_k,

                        document_types=request.document_types,

                        departments=request.departments,

                        include_sources=request.include_sources
                    )

                execution_time = time.perf_counter() - start_ts
                usage_values = usage.as_dict()

                # Log configuration and actual usage separately.
                mlflow.log_param("llm_model", usage_values["model"])
                mlflow.log_param(
                    "input_price_per_1m_usd", INPUT_PRICE_PER_1M
                )
                mlflow.log_param(
                    "output_price_per_1m_usd", OUTPUT_PRICE_PER_1M
                )
                mlflow.log_param("input", request)
                mlflow.log_param("output", response)
                mlflow.log_param("execution_time", execution_time)

                metric_names = (
                    "input_tokens",
                    "output_tokens",
                    "total_tokens",
                    "input_cost_usd",
                    "output_cost_usd",
                    "total_cost_usd",
                    "llm_call_count",
                    "usage_reported_call_count",
                )
                for metric_name in metric_names:
                    mlflow.log_metric(
                        metric_name,
                        float(usage_values[metric_name])
                    )

                mlflow.log_metric(
                    "execution_time_seconds",
                    round(execution_time, 4)
                )

                mlflow.set_tag("llm_usage_source", usage_values["source"])
                mlflow.log_param("end_time", datetime.now().isoformat())

                logger.info(
                    "LLM usage captured: "
                    f"model={usage_values['model']}, "
                    f"input_tokens={usage_values['input_tokens']}, "
                    f"output_tokens={usage_values['output_tokens']}, "
                    f"total_tokens={usage_values['total_tokens']}, "
                    f"input_cost_usd={usage_values['input_cost_usd']:.15f}, "
                    f"output_cost_usd={usage_values['output_cost_usd']:.15f}, "
                    f"total_cost_usd={usage_values['total_cost_usd']:.15f}, "
                    f"llm_call_count={usage_values['llm_call_count']}, "
                    f"usage_reported_call_count="
                    f"{usage_values['usage_reported_call_count']}"
                )

                if usage_values["usage_reported_call_count"] == 0:
                    logger.warning(
                        "No token usage was reported by the AutoGen model "
                        "client. Check that MonitoringImplementation uses "
                        "settings.get_model_client() and that the provider "
                        "returns usage metadata."
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