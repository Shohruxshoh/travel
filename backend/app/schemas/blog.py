"""Pydantic schemas for Blog Articles."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BlogBase(BaseModel):
    title_ru: str = Field(..., max_length=255)
    title_en: str = Field(..., max_length=255)
    title_fr: str = Field(..., max_length=255)
    content_ru: str
    content_en: str
    content_fr: str
    slug: str = Field(..., max_length=255)
    cover_image: Optional[str] = None
    author: Optional[str] = None
    is_published: bool = False


class BlogCreate(BlogBase):
    pass


class BlogResponse(BlogBase):
    id: int
    published_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
