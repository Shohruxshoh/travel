"""
Blog Article Model
------------------
Articles, news, and useful information for tourists.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class BlogArticle(Base):
    """Blog post with multilingual content."""

    __tablename__ = "blog_articles"

    id = Column(Integer, primary_key=True, index=True)

    # ── Multilingual title ───────────────────────────────────────
    title_ru = Column(String(255), nullable=False, comment="Title in Russian")
    title_en = Column(String(255), nullable=False, comment="Title in English")
    title_fr = Column(String(255), nullable=False, comment="Title in French")

    # ── Multilingual content ─────────────────────────────────────
    content_ru = Column(Text, nullable=False, comment="Full article body in Russian")
    content_en = Column(Text, nullable=False, comment="Full article body in English")
    content_fr = Column(Text, nullable=False, comment="Full article body in French")

    # ── SEO & media ──────────────────────────────────────────────
    slug = Column(String(255), unique=True, nullable=False, index=True, comment="URL-friendly slug")
    cover_image = Column(String(512), nullable=True, comment="Cover image URL")

    # ── Metadata ─────────────────────────────────────────────────
    author = Column(String(255), nullable=True, comment="Author name")
    is_published = Column(Boolean, default=False, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<BlogArticle(id={self.id}, slug='{self.slug}')>"
