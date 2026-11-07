from pydantic import BaseModel, Field
from typing import List, Optional


class ChatHistory(BaseModel):
    role: str = Field(
        ...,
        description="user | assistant"
    )
    content: str


class RAGRequest(BaseModel):

    question: str = Field(
        ...,
        description="Healthcare question from user"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of documents to retrieve"
    )

    document_types: Optional[List[str]] = Field(
        default=None,
        description="""
        guideline
        sop
        protocol
        """
    )

    departments: Optional[List[str]] = Field(
        default=None,
        description="""
        cardiology
        endocrinology
        oncology
        pulmonology
        nephrology
        neurology
        psychiatry
        """
    )

    document_names: Optional[List[str]] = Field(
        default=None,
        description="Specific documents to search"
    )

    include_sources: bool = Field(
        default=True,
        description="Return source references"
    )

    conversation_history: Optional[
        List[ChatHistory]
    ] = None