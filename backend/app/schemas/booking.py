"""
Pydantic schemas for Bookings.
Includes the critical 'language' field for smart email routing.
"""

from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional, Any
from datetime import datetime


class BookingCreate(BaseModel):
    """
    Schema for creating a booking.
    The 'language' field is sent from the Vue frontend
    based on the user's currently selected locale.
    """
    tour_id: int = Field(..., gt=0)
    customer_name: str = Field(..., min_length=2, max_length=255)
    customer_email: EmailStr
    customer_phone: Optional[str] = Field(None, max_length=50)
    message: Optional[str] = None
    language: str = Field(
        default="en",
        pattern="^(ru|en|fr)$",
        description="User's selected language — determines which operator is notified"
    )


class BookingResponse(BaseModel):
    """Schema for booking response."""
    id: int
    tour_id: int
    tour_title: Optional[str] = None
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    message: Optional[str] = None
    language: str
    status: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def extract_tour_title(cls, data: Any) -> Any:
        """Extract tour title from the loaded tour relationship."""
        if hasattr(data, "tour") and data.tour:
            data.tour_title = data.tour.title_en or ""
        return data


class OperatorConfigBase(BaseModel):
    """Schema for language-operator config management (Admin panel)."""
    language_code: str = Field(..., pattern="^(ru|en|fr)$")
    operator_name: str = Field(..., max_length=255)
    operator_email: EmailStr
    is_active: bool = True


class OperatorConfigCreate(OperatorConfigBase):
    pass


class OperatorConfigUpdate(BaseModel):
    operator_name: Optional[str] = None
    operator_email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class OperatorConfigResponse(OperatorConfigBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
