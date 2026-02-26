"""
Celery Application Configuration
---------------------------------
Creates and configures the Celery instance with Redis as broker.
"""

from celery import Celery
from app.config import get_settings

settings = get_settings()

# ── Create Celery instance ───────────────────────────────────────
celery_app = Celery(
    "travel_agency",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.email_tasks"],  # Auto-discover task modules
)

# ── Celery configuration ────────────────────────────────────────
celery_app.conf.update(
    # Serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    # Timezone
    timezone="UTC",
    enable_utc=True,

    # Retry policy for broker connection
    broker_connection_retry_on_startup=True,

    # Task execution limits
    task_soft_time_limit=60,      # Soft limit: 60 seconds
    task_time_limit=120,          # Hard limit: 2 minutes
    task_acks_late=True,          # Acknowledge after execution (reliability)

    # Result expiry
    result_expires=3600,          # Results expire after 1 hour
)
