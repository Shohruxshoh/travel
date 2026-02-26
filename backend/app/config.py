"""
Application Configuration
-------------------------
Centralized settings loaded from environment variables via Pydantic BaseSettings.
All sensitive values (DB credentials, SMTP passwords, etc.) are read from .env file.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable loading."""

    # ── Application ──────────────────────────────────────────────
    APP_NAME: str = "Travel Agency API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    # ── Database (PostgreSQL) ────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://travel_user:travel_pass@localhost:5432/travel_db"

    # ── Redis (Celery broker) ────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── SMTP (Email sending) ────────────────────────────────────
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@travelagency.com"
    SMTP_USE_TLS: bool = True

    # ── Director email (always receives booking notifications) ───
    DIRECTOR_EMAIL: str = "director@travelagency.com"

    # ── Site URL (for links in emails) ────────────────────────────
    SITE_URL: str = "http://localhost:5173"

    # ── Supported languages ──────────────────────────────────────
    SUPPORTED_LANGUAGES: list[str] = ["ru", "en", "fr"]

    # ── Admin Auth ───────────────────────────────────────────────
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin2026"
    JWT_SECRET_KEY: str = "adventures-travel-time-secret-key-change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 480  # 8 hours

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton to avoid re-reading .env on every request."""
    return Settings()
