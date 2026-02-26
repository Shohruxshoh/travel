"""
Language Operator Configuration Model
-------------------------------------
Maps language codes to tour operator email addresses.
Managed via Admin panel — never hardcoded.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class LanguageOperatorConfig(Base):
    """
    Database-driven configuration mapping each supported language
    to the tour operator responsible for that language.

    Example rows:
        language_code='en' → operator_email='john@agency.com'
        language_code='ru' → operator_email='ivan@agency.com'
        language_code='fr' → operator_email='marie@agency.com'
    """

    __tablename__ = "language_operator_configs"

    id = Column(Integer, primary_key=True, index=True)

    # ── Language mapping ─────────────────────────────────────────
    language_code = Column(
        String(5),
        unique=True,
        nullable=False,
        index=True,
        comment="ISO language code: ru, en, or fr"
    )
    operator_name = Column(
        String(255),
        nullable=False,
        comment="Name of the operator for this language"
    )
    operator_email = Column(
        String(255),
        nullable=False,
        comment="Email address of the responsible operator"
    )

    # ── Status ───────────────────────────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<LanguageOperatorConfig(lang='{self.language_code}', email='{self.operator_email}')>"
