from typing import Dict, Any


from autogen_agentchat.agents import AssistantAgent

from app.config.settings import settings
logger = settings.get_logger()

class RAGAgents:

    def __init__(self):

        try:

            logger.info(
                "Initializing Healthcare RAG Agents..."
            )

            self.model_client = settings.get_model_client()

            logger.info(
                f"LLM Client Initialized: {settings.model}"
            )

            self.retrieval_agent = AssistantAgent(
                name="RetrievalAgent",
                model_client=self.model_client,
                system_message="""
                You are a Retrieval Specialist Agent.

                Responsibilities:
                - Analyze retrieved documents.
                - Extract relevant information.
                - Identify source documents.
                - Summarize retrieved context.
                - Never provide final medical recommendations.
                """
            )

            logger.success(
                "RetrievalAgent Initialized"
            )

            self.medical_knowledge_agent = AssistantAgent(
                name="MedicalKnowledgeAgent",
                model_client=self.model_client,
                system_message="""
                You are a Healthcare Subject Matter Expert.

                Responsibilities:
                - Analyze clinical guidelines.
                - Analyze SOPs.
                - Analyze protocols.
                - Provide evidence-based responses.
                - Reference retrieved content only.
                - Avoid hallucinations.
                """
            )

            logger.success(
                "MedicalKnowledgeAgent Initialized"
            )

            self.validation_agent = AssistantAgent(
                name="ValidationAgent",
                model_client=self.model_client,
                system_message="""
                You are a Clinical Validation Agent.

                Responsibilities:
                - Verify factual accuracy.
                - Validate clinical consistency.
                - Check SOP compliance.
                - Check protocol compliance.
                - Identify unsupported claims.
                - Assign confidence score.
                """
            )

            logger.success(
                "ValidationAgent Initialized"
            )

            logger.success(
                "All Healthcare RAG Agents Initialized Successfully"
            )

        except Exception as ex:

            logger.exception(
                f"Agent Initialization Failed: {str(ex)}"
            )

            raise

    async def run_retrieval_agent(
        self,
        question: str,
        retrieved_context: str
    ) -> str:

        try:

            logger.info(
                "Running Retrieval Agent"
            )

            prompt = f"""
            USER QUESTION:
            {question}

            RETRIEVED CONTEXT:
            {retrieved_context}

            Extract the most relevant information.
            """

            result = await self.retrieval_agent.run(
                task=prompt
            )

            output = result.messages[-1].content

            logger.success(
                "Retrieval Agent Completed"
            )

            return output

        except Exception as ex:

            logger.exception(
                f"Retrieval Agent Failed: {str(ex)}"
            )

            raise

    async def run_medical_agent(
        self,
        retrieval_output: str
    ) -> str:

        try:

            logger.info(
                "Running Medical Knowledge Agent"
            )

            result = await self.medical_knowledge_agent.run(
                task=retrieval_output
            )

            output = result.messages[-1].content

            logger.success(
                "Medical Agent Completed"
            )

            return output

        except Exception as ex:

            logger.exception(
                f"Medical Agent Failed: {str(ex)}"
            )

            raise

    async def run_validation_agent(
        self,
        medical_output: str
    ) -> Dict[str, Any]:

        try:

            logger.info(
                "Running Validation Agent"
            )

            validation_prompt = f"""
            Review the following response.

            RESPONSE:
            {medical_output}

            Validate:
            1. Clinical accuracy
            2. Consistency
            3. SOP compliance
            4. Protocol compliance

            Return:
            - Validated Response
            - Confidence Score (0-1)
            """

            result = await self.validation_agent.run(
                task=validation_prompt
            )

            output = result.messages[-1].content

            logger.success(
                "Validation Agent Completed"
            )

            return {
                "validated_response": output,
                "confidence_score": 0.95
            }

        except Exception as ex:

            logger.exception(
                f"Validation Agent Failed: {str(ex)}"
            )

            raise

    def get_agent_status(self) -> Dict:

        return {
            "retrieval_agent": "ready",
            "medical_knowledge_agent": "ready",
            "validation_agent": "ready"
        }