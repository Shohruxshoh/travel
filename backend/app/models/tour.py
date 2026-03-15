"""
Tour Package Model
------------------
Represents a travel tour offered by the agency.
Multilingual fields (title, description) use _ru/_en/_fr suffixes.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class TourPackage(Base):
    """Tour package with multilingual content and pricing."""

    __tablename__ = "tour_packages"

    id = Column(Integer, primary_key=True, index=True)

    # ── Multilingual title ───────────────────────────────────────
    title_ru = Column(String(255), nullable=False, comment="Tour title in Russian")
    title_en = Column(String(255), nullable=False, comment="Tour title in English")
    title_fr = Column(String(255), nullable=False, comment="Tour title in French")

    # ── Multilingual description ─────────────────────────────────
    description_ru = Column(Text, nullable=False, comment="Full description in Russian")
    description_en = Column(Text, nullable=False, comment="Full description in English")
    description_fr = Column(Text, nullable=False, comment="Full description in French")

    # ── Tour category ─────────────────────────────────────────────
    category = Column(
        String(20), nullable=False, default="full",
        comment="Tour type: 'full' (full tour) or 'extra' (additional tour)"
    )

    # ── Tour details ─────────────────────────────────────────────
    price = Column(Numeric(10, 2), nullable=True, comment="Price in EUR, NULL if negotiable")
    is_negotiable = Column(
        Boolean, default=False, nullable=False,
        comment="If true, price is 'negotiable' instead of fixed"
    )
    duration_days = Column(Integer, nullable=False, comment="Duration in days")
    destination = Column(String(255), nullable=False, comment="Destination city/country")

    # ── JSON fields for flexible data ────────────────────────────
    itinerary_json = Column(
        JSON, nullable=True,
        comment="Day-by-day itinerary as JSON array"
    )
    images_json = Column(
        JSON, nullable=True,
        comment="Array of image URLs for the tour"
    )
    cover_image = Column(String(512), nullable=True, comment="Main cover image URL")

    # ── Status ───────────────────────────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ── Relationships ────────────────────────────────────────────
    bookings = relationship("Booking", back_populates="tour", lazy="selectin")
    gallery_items = relationship("GalleryItem", back_populates="tour", lazy="selectin")

    def __repr__(self):
        return f"<TourPackage(id={self.id}, title_en='{self.title_en}')>"
