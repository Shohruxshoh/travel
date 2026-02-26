"""
Booking Model
-------------
Customer booking for a tour package.
Stores the language used at booking time for email routing.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class BookingStatus(str, enum.Enum):
    """Status lifecycle for a booking."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(Base):
    """
    Tour booking with language-aware email notification routing.
    The 'language' field determines which operator receives the notification.
    """

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    # ── Tour association ─────────────────────────────────────────
    tour_id = Column(
        Integer,
        ForeignKey("tour_packages.id", ondelete="CASCADE"),
        nullable=False,
        comment="Booked tour package"
    )

    # ── Customer information ─────────────────────────────────────
    customer_name = Column(String(255), nullable=False, comment="Full name")
    customer_email = Column(String(255), nullable=False, comment="Contact email")
    customer_phone = Column(String(50), nullable=True, comment="Phone number")
    message = Column(Text, nullable=True, comment="Additional message or requests")

    # ── Language for smart email routing ─────────────────────────
    language = Column(
        String(5),
        nullable=False,
        default="en",
        comment="Language code (ru, en, fr) — determines which operator is notified"
    )

    # ── Booking status ───────────────────────────────────────────
    status = Column(
        Enum(BookingStatus, name="booking_status_enum"),
        default=BookingStatus.PENDING,
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ── Relationships ────────────────────────────────────────────
    tour = relationship("TourPackage", back_populates="bookings")

    def __repr__(self):
        return f"<Booking(id={self.id}, tour_id={self.tour_id}, lang='{self.language}')>"
