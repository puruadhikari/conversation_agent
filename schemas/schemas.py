#from __future__ import annotations

from typing import TypedDict, List
from pydantic import BaseModel, Field


class JourneyClassificationOutput(BaseModel):
    """Structured output for journey classification (single LLM call)."""

    journey: str = Field(description="Top-level customer journey category, e.g. 'Payment'.")
    sub_journey: str = Field(
        description="Specific sub-journey label (one of ~150 predefined items), e.g. 'View Payment'."
    )


class DocumentRetrievalOutput(BaseModel):
    """Structured output containing relevant knowledge-base documents."""

    document_ids: List[str] = Field(
        default_factory=list,
        description="List of document identifiers or URLs relevant to the conversation.",
    )


class CrossSellOutput(BaseModel):
    """Structured output with cross-sell recommendations."""

    suggested_items: List[str] = Field(
        default_factory=list,
        description="List of recommended cross-sell products/services (identifiers or SKUs).",
    )


class ConversationAnalysisState(TypedDict):
    """State object carried through the LangGraph workflow."""

    conversation: str  # Pre-processed recent dialogue snippet
    journey: str  # High-level journey
    sub_journey: str  # Specific sub-journey (from 150)
    retrieved_documents: List[str]  # Docs pulled from KB
    cross_sell_opportunities: List[str]  # Suggested cross-sell items