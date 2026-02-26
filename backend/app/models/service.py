"""
Service Model
-------------
Represents additional agency services (visas, insurance, transfers).
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Service(Base):
    """Additional travel service offered by the agency."""

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    # ── Multilingual name ────────────────────────────────────────
    name_ru = Column(String(255), nullable=False, comment="Service name in Russian")
    name_en = Column(String(255), nullable=False, comment="Service name in English")
    name_fr = Column(String(255), nullable=False, comment="Service name in French")

    # ── Multilingual description ─────────────────────────────────
    description_ru = Column(Text, nullable=True, comment="Description in Russian")
    description_en = Column(Text, nullable=True, comment="Description in English")
    description_fr = Column(Text, nullable=True, comment="Description in French")

    # ── Details ──────────────────────────────────────────────────
    price = Column(Numeric(10, 2), nullable=True, comment="Price in USD (null = varies)")
    icon = Column(String(100), nullable=True, comment="Icon class or URL")

    # ── Status ───────────────────────────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Service(id={self.id}, name_en='{self.name_en}')>"
