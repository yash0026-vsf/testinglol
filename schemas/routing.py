from typing import Literal

from pydantic import BaseModel, Field


class IntentClassification(BaseModel):
    intent: Literal[
        "billing",
        "technical",
        "account",
        "general",
        "complaint",
        "unknown",
    ] = Field(
        description="The customer support intent detected from the message."
    )
    sentiment: Literal["positive", "neutral", "negative"] = Field(
        description="The sentiment of the customer message."
    )
    urgency: Literal["low", "medium", "high", "critical"] = Field(
        description="The urgency of the customer request based on tone and impact."
    )
    language: str = Field(
        description="The detected language of the customer's message (e.g., 'English', 'Spanish')."
    )