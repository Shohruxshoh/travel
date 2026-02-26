"""Pydantic schemas for Hotels."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class HotelBase(BaseModel):
    name: str = Field(..., max_length=255)
    city: str = Field(..., max_length=255)
    country: str = Field(..., max_length=255)
    star_rating: int = Field(..., ge=1, le=5)
    image_url: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    description_fr: Optional[str] = None
    room_types_json: Optional[list[dict]] = None
    price_from: float = Field(..., gt=0)
    is_active: bool = True


class HotelCreate(HotelBase):
    pass


class HotelResponse(HotelBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
