"""Pydantic schemas for Services."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ServiceBase(BaseModel):
    name_ru: str = Field(..., max_length=255)
    name_en: str = Field(..., max_length=255)
    name_fr: str = Field(..., max_length=255)
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    description_fr: Optional[str] = None
    price: Optional[float] = None
    icon: Optional[str] = None
    is_active: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
