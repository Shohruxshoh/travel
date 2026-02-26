"""
Pydantic schemas for Bookings.
Includes the critical 'language' field for smart email routing.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
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
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    message: Optional[str] = None
    language: str
    status: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


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
