from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class SourceDocument(BaseModel):

    document_name: str

    document_type: str

    department: Optional[str] = None

    version: Optional[str] = None

    relevance_score: float

    excerpt: Optional[str] = None


class AgentResponse(BaseModel):

    agent_name: str

    output: str


class RetrievalMetadata(BaseModel):

    retrieved_documents: int

    top_k: int

    retrieval_time_seconds: float


class ValidationResult(BaseModel):

    is_valid: bool

    confidence_score: float

    validation_notes: Optional[str] = None


class RAGResponse(BaseModel):

    success: bool

    question: str

    answer: str

    validation: ValidationResult

    retrieval_metadata: RetrievalMetadata

    sources: List[SourceDocument]

    agent_outputs: List[AgentResponse]

    session_id: Optional[str] = None

    execution_time_seconds: float

    message: str