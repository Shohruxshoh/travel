"""Pydantic schemas for Comments."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CommentCreate(BaseModel):
    """Schema for creating a new comment."""
    author_name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    tour_id: Optional[int] = None
    image_url: Optional[str] = Field(None, max_length=512)


class CommentResponse(BaseModel):
    """Schema for comment response."""
    id: int
    author_name: str
    country: str
    description: str
    image_url: Optional[str] = None
    tour_id: Optional[int] = None
    approved: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
