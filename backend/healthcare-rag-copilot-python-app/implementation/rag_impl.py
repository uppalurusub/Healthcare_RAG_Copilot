import time
from typing import List

from utils.logger import logger

from memory.vector_store import VectorStore
from agents.rag_agents import RAGAgents

from models.response_model import (
    RAGResponse,
    SourceDocument,
    AgentResponse,
    ValidationResult,
    RetrievalMetadata
)


class RAGImplementation:

    def __init__(self):

        logger.info(
            "Initializing Healthcare RAG Implementation"
        )

        self.vector_store = VectorStore()

        self.agents = RAGAgents()

        logger.success(
            "Healthcare RAG Implementation Initialized"
        )

    async def ask_question(
        self,
        question: str,
        top_k: int = 5,
        document_types: List[str] | None = None,
        departments: List[str] | None = None,
        include_sources: bool = True
    ) -> RAGResponse:

        start_time = time.time()

        try:

            logger.info(
                f"Healthcare Question Received: {question}"
            )

            # --------------------------------------------------
            # Step 1: Retrieve Documents
            # --------------------------------------------------

            logger.info(
                "Searching Knowledge Base"
            )

            search_result = self.vector_store.search(
                query=question,
                top_k=top_k
            )

            if not search_result["success"]:

                logger.error(
                    "Vector Search Failed"
                )

                return RAGResponse(
                    success=False,
                    question=question,
                    answer="",
                    validation=ValidationResult(
                        is_valid=False,
                        confidence_score=0.0,
                        validation_notes="Search Failed"
                    ),
                    retrieval_metadata=RetrievalMetadata(
                        retrieved_documents=0,
                        top_k=top_k,
                        retrieval_time_seconds=0.0
                    ),
                    sources=[],
                    agent_outputs=[],
                    execution_time_seconds=0,
                    message="Knowledge base search failed"
                )

            retrieved_docs = search_result.get(
                "documents",
                []
            )

            retrieved_metadata = search_result.get(
                "metadatas",
                []
            )

            retrieved_distances = search_result.get(
                "distances",
                []
            )

            if not retrieved_docs:

                logger.warning(
                    "No Documents Retrieved"
                )

                return RAGResponse(
                    success=False,
                    question=question,
                    answer="",
                    validation=ValidationResult(
                        is_valid=False,
                        confidence_score=0.0,
                        validation_notes="No evidence found"
                    ),
                    retrieval_metadata=RetrievalMetadata(
                        retrieved_documents=0,
                        top_k=top_k,
                        retrieval_time_seconds=0
                    ),
                    sources=[],
                    agent_outputs=[],
                    execution_time_seconds=0,
                    message="No relevant documents found"
                )

            logger.success(
                f"Retrieved {len(retrieved_docs)} documents"
            )

            # --------------------------------------------------
            # Step 2: Build Context
            # --------------------------------------------------

            context = "\n\n".join(
                retrieved_docs
            )

            logger.info(
                "Running Retrieval Agent"
            )

            retrieval_output = (
                await self.agents.run_retrieval_agent(
                    question=question,
                    retrieved_context=context
                )
            )

            logger.success(
                "Retrieval Agent Completed"
            )

            # --------------------------------------------------
            # Step 3: Medical Agent
            # --------------------------------------------------

            logger.info(
                "Running Medical Agent"
            )

            medical_output = (
                await self.agents.run_medical_agent(
                    retrieval_output
                )
            )

            logger.success(
                "Medical Agent Completed"
            )

            # --------------------------------------------------
            # Step 4: Validation Agent
            # --------------------------------------------------

            logger.info(
                "Running Validation Agent"
            )

            validation_output = (
                await self.agents.run_validation_agent(
                    medical_output
                )
            )

            logger.success(
                "Validation Agent Completed"
            )

            # --------------------------------------------------
            # Step 5: Source Documents
            # --------------------------------------------------

            source_documents = []

            if include_sources:

                for idx, metadata in enumerate(
                    retrieved_metadata
                ):

                    score = 0.0

                    if idx < len(
                        retrieved_distances
                    ):
                        score = round(
                            1 -
                            float(
                                retrieved_distances[idx]
                            ),
                            4
                        )

                    source_documents.append(
                        SourceDocument(
                            document_name=
                            metadata.get(
                                "document_name",
                                f"Doc_{idx+1}"
                            ),

                            document_type=
                            metadata.get(
                                "document_type",
                                "unknown"
                            ),

                            department=
                            metadata.get(
                                "department"
                            ),

                            version=
                            metadata.get(
                                "version"
                            ),

                            relevance_score=
                            max(score, 0),

                            excerpt=
                            retrieved_docs[idx][:250]
                        )
                    )

            # --------------------------------------------------
            # Step 6: Agent Outputs
            # --------------------------------------------------

            agent_outputs = [

                AgentResponse(
                    agent_name="RetrievalAgent",
                    output=retrieval_output
                ),

                AgentResponse(
                    agent_name=
                    "MedicalKnowledgeAgent",
                    output=medical_output
                ),

                AgentResponse(
                    agent_name=
                    "ValidationAgent",
                    output=validation_output[
                        "validated_response"
                    ]
                )
            ]

            execution_time = round(
                time.time() - start_time,
                2
            )

            logger.success(
                f"Healthcare RAG Completed in "
                f"{execution_time} seconds"
            )

            return RAGResponse(

                success=True,

                question=question,

                answer=validation_output[
                    "validated_response"
                ],

                validation=ValidationResult(
                    is_valid=True,
                    confidence_score=
                    validation_output.get(
                        "confidence_score",
                        0.95
                    ),
                    validation_notes=
                    "Validated successfully"
                ),

                retrieval_metadata=
                RetrievalMetadata(
                    retrieved_documents=
                    len(retrieved_docs),
                    top_k=top_k,
                    retrieval_time_seconds=
                    search_result.get(
                        "retrieval_time_seconds",
                        0
                    )
                ),

                sources=source_documents,

                agent_outputs=agent_outputs,

                execution_time_seconds=
                execution_time,

                message=
                "Healthcare RAG response generated successfully"
            )

        except Exception as ex:

            logger.exception(
                f"Healthcare RAG Failed: {str(ex)}"
            )

            execution_time = round(
                time.time() - start_time,
                2
            )

            return RAGResponse(
                success=False,
                question=question,
                answer="",

                validation=ValidationResult(
                    is_valid=False,
                    confidence_score=0.0,
                    validation_notes=str(ex)
                ),

                retrieval_metadata=
                RetrievalMetadata(
                    retrieved_documents=0,
                    top_k=top_k,
                    retrieval_time_seconds=0
                ),

                sources=[],

                agent_outputs=[],

                execution_time_seconds=
                execution_time,

                message=str(ex)
            )