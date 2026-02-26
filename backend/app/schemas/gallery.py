"""Pydantic schemas for Gallery Items."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GalleryBase(BaseModel):
    media_type: str = Field(..., pattern="^(image|video)$")
    url: str = Field(..., max_length=512)
    thumbnail_url: Optional[str] = None
    caption_ru: Optional[str] = None
    caption_en: Optional[str] = None
    caption_fr: Optional[str] = None
    tour_id: Optional[int] = None
    sort_order: int = 0


class GalleryCreate(GalleryBase):
    pass


class GalleryResponse(GalleryBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
