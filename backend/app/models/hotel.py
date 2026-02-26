"""
Hotel Model
-----------
Represents hotel listings with star ratings, room types, and pricing.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Hotel(Base):
    """Hotel listing with ratings and room information."""

    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)

    # ── Basic info ───────────────────────────────────────────────
    name = Column(String(255), nullable=False, comment="Hotel name")
    city = Column(String(255), nullable=False, comment="City location")
    country = Column(String(255), nullable=False, comment="Country")
    star_rating = Column(Integer, nullable=False, comment="Star rating 1-5")
    image_url = Column(String(512), nullable=True, comment="Main hotel image URL")

    # ── Multilingual description ─────────────────────────────────
    description_ru = Column(Text, nullable=True, comment="Description in Russian")
    description_en = Column(Text, nullable=True, comment="Description in English")
    description_fr = Column(Text, nullable=True, comment="Description in French")

    # ── Room types stored as JSON for flexibility ────────────────
    room_types_json = Column(
        JSON, nullable=True,
        comment='Array of objects: [{"type": "Standard", "price": 100, "capacity": 2}]'
    )

    # ── Pricing ──────────────────────────────────────────────────
    price_from = Column(Numeric(10, 2), nullable=False, comment="Starting price per night in USD")

    # ── Status ───────────────────────────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Hotel(id={self.id}, name='{self.name}', stars={self.star_rating})>"
