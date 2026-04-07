"""Chat request/response schema objects."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming chat request payload."""

    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    """Outgoing chat response payload."""

    response: str
    provider: str
    model: str
