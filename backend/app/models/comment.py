"""
Comment Model
-------------
Represents a public comment/review left by site visitors.
Comments are visible to all users without authentication.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Comment(Base):
    """Public comment/review submitted by visitors."""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    # ── Optional relation to a tour ──────────────────────────────
    tour_id = Column(
        Integer, ForeignKey("tour_packages.id", ondelete="CASCADE"),
        nullable=True, index=True,
        comment="If set, comment belongs to a specific tour; NULL = general review"
    )

    # ── Author info ───────────────────────────────────────────────
    author_name = Column(String(100), nullable=False, comment="Visitor's display name")
    country = Column(String(100), nullable=False, comment="Visitor's country name")

    # ── Content ───────────────────────────────────────────────────
    description = Column(Text, nullable=False, comment="Comment text")
    image_url = Column(String(512), nullable=True, comment="Optional photo URL")

    # ── Moderation ───────────────────────────────────────────────
    approved = Column(
        Boolean, default=True, nullable=False,
        comment="Visible to public when True"
    )

    # ── Timestamps ───────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<Comment(id={self.id}, author='{self.author_name}', tour_id={self.tour_id})>"
