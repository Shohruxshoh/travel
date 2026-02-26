"""
Gallery Item Model
------------------
High-quality images and videos from previous trips.
Optionally linked to a TourPackage.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class MediaType(str, enum.Enum):
    """Supported media types for gallery items."""
    IMAGE = "image"
    VIDEO = "video"


class GalleryItem(Base):
    """Media item (image or video) in the agency gallery."""

    __tablename__ = "gallery_items"

    id = Column(Integer, primary_key=True, index=True)

    # ── Media info ───────────────────────────────────────────────
    media_type = Column(
        Enum(MediaType, name="media_type_enum"),
        nullable=False,
        comment="Type of media: image or video"
    )
    url = Column(String(512), nullable=False, comment="URL to the media file")
    thumbnail_url = Column(String(512), nullable=True, comment="Thumbnail URL for videos")

    # ── Multilingual captions ────────────────────────────────────
    caption_ru = Column(String(500), nullable=True, comment="Caption in Russian")
    caption_en = Column(String(500), nullable=True, comment="Caption in English")
    caption_fr = Column(String(500), nullable=True, comment="Caption in French")

    # ── Optional tour association ────────────────────────────────
    tour_id = Column(
        Integer,
        ForeignKey("tour_packages.id", ondelete="SET NULL"),
        nullable=True,
        comment="Associated tour package (optional)"
    )

    # ── Metadata ─────────────────────────────────────────────────
    sort_order = Column(Integer, default=0, comment="Display order")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ── Relationships ────────────────────────────────────────────
    tour = relationship("TourPackage", back_populates="gallery_items")

    def __repr__(self):
        return f"<GalleryItem(id={self.id}, type='{self.media_type}')>"
