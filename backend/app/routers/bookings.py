"""
Bookings API Router
-------------------
POST /bookings — Creates a booking and triggers the Celery
email notification task with smart language-based routing.
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging

from app.database import get_db
from app.models.tour import TourPackage
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingResponse
from app.tasks.email_tasks import send_booking_notification

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/", response_model=list[BookingResponse])
async def list_bookings(db: AsyncSession = Depends(get_db)):
    """List all bookings (for admin dashboard)."""
    result = await db.execute(
        select(Booking).order_by(Booking.created_at.desc()).limit(100)
    )
    return result.scalars().all()


@router.post("/", response_model=BookingResponse, status_code=201)
async def create_booking(
    booking_data: BookingCreate,
    accept_language: Optional[str] = Header(None, alias="Accept-Language"),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new tour booking.

    Smart Email Routing Flow:
    1. Client sends booking with 'language' field (from vue-i18n locale).
    2. We also read the Accept-Language header as a fallback.
    3. The booking is saved to PostgreSQL.
    4. A Celery background task is dispatched to:
       - Look up the LanguageOperatorConfig for the booking's language.
       - Send notification emails to the language operator AND the director.
    """
    # ── Validate that the tour exists ────────────────────────────
    tour_result = await db.execute(
        select(TourPackage).where(TourPackage.id == booking_data.tour_id)
    )
    tour = tour_result.scalar_one_or_none()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour package not found")

    if not tour.is_active:
        raise HTTPException(status_code=400, detail="This tour is no longer available")

    # ── Determine language (payload takes priority over header) ──
    language = booking_data.language
    if not language and accept_language:
        # Parse Accept-Language header (e.g., "en-US,en;q=0.9,fr;q=0.8")
        language = accept_language.split(",")[0].split("-")[0].lower()
    if language not in ("ru", "en", "fr"):
        language = "en"  # Default fallback

    # ── Create the booking record ────────────────────────────────
    new_booking = Booking(
        tour_id=booking_data.tour_id,
        customer_name=booking_data.customer_name,
        customer_email=booking_data.customer_email,
        customer_phone=booking_data.customer_phone,
        message=booking_data.message,
        language=language,
    )
    db.add(new_booking)
    await db.flush()       # Get the auto-generated ID
    await db.refresh(new_booking)

    # ── Dispatch Celery background task for email notifications ──
    try:
        send_booking_notification.delay(new_booking.id)
        logger.info(
            f"Booking #{new_booking.id} created. "
            f"Email task dispatched for language='{language}'."
        )
    except Exception as e:
        # Don't fail the booking if email dispatch fails
        logger.error(f"Failed to dispatch email task for booking #{new_booking.id}: {e}")

    return new_booking
