"""Validated API request and response models."""

from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    response: str
    provider: str
    model: str


class ContactRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    company: str | None = Field(default=None, max_length=120)
    message: str = Field(min_length=10, max_length=3000)
    privacy_accepted: Literal[True]
    website: str = Field(default="", max_length=200)


class ContactResponse(BaseModel):
    status: Literal["accepted"] = "accepted"
    message: str
    delivery: Literal["stored", "stored_and_emailed"]
