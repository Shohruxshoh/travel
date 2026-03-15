"""Pydantic schemas for Tour Packages."""

from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
from datetime import datetime


class TourBase(BaseModel):
    """Shared fields for tour creation and updates."""
    title_ru: str = Field(..., max_length=255)
    title_en: str = Field(..., max_length=255)
    title_fr: str = Field(..., max_length=255)
    description_ru: str
    description_en: str
    description_fr: str
    category: Literal["full", "extra"] = "full"
    price: Optional[float] = Field(None, gt=0)
    is_negotiable: bool = False

    @model_validator(mode="after")
    def check_price_or_negotiable(self):
        """Price is required unless is_negotiable is True."""
        if not self.is_negotiable and self.price is None:
            raise ValueError("Price is required when tour is not negotiable")
        if self.is_negotiable:
            self.price = None
        return self
    duration_days: int = Field(..., gt=0)
    destination: str = Field(..., max_length=255)
    itinerary_json: Optional[list[dict]] = None
    images_json: Optional[list[str]] = None
    cover_image: Optional[str] = None
    is_active: bool = True


class TourCreate(TourBase):
    """Schema for creating a new tour."""
    pass


class TourUpdate(BaseModel):
    """Schema for partial tour updates (all fields optional)."""
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    title_fr: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    description_fr: Optional[str] = None
    category: Optional[Literal["full", "extra"]] = None
    price: Optional[float] = None
    is_negotiable: Optional[bool] = None
    duration_days: Optional[int] = None
    destination: Optional[str] = None
    itinerary_json: Optional[list[dict]] = None
    images_json: Optional[list[str]] = None
    cover_image: Optional[str] = None
    is_active: Optional[bool] = None


class TourResponse(TourBase):
    """Schema for tour response with database fields."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
