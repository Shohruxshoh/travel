"""
Email Notification Tasks (Celery)
---------------------------------
Smart email routing:
1. When a booking is created, this task is triggered asynchronously.
2. It looks up the LanguageOperatorConfig for the booking's language.
3. Sends notification emails to:
   a) The language-specific tour operator
   b) The agency director
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.tasks.celery_app import celery_app
from app.config import get_settings
from app.models.booking import Booking
from app.models.tour import TourPackage
from app.models.operator_config import LanguageOperatorConfig
from app.database import Base

logger = logging.getLogger(__name__)
settings = get_settings()

# ── Synchronous engine for Celery workers ────────────────────────
# Celery tasks run in a sync context, so we use a regular
# (non-async) SQLAlchemy engine here.
SYNC_DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql+asyncpg://", "postgresql+psycopg2://"
)
sync_engine = create_engine(SYNC_DATABASE_URL, pool_pre_ping=True)


def _build_email_html(booking: Booking, tour: TourPackage) -> str:
    """Build a professional HTML email body for booking notification."""
    tour_url = f"{settings.SITE_URL}/tours/{tour.id}"
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                🌍 New Booking Notification
            </h2>

            <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <tr>
                    <td style="padding: 8px; font-weight: bold; color: #555;">Booking ID:</td>
                    <td style="padding: 8px;">#{booking.id}</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="padding: 8px; font-weight: bold; color: #555;">Tour:</td>
                    <td style="padding: 8px;">{tour.title_en}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold; color: #555;">Customer:</td>
                    <td style="padding: 8px;">{booking.customer_name}</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="padding: 8px; font-weight: bold; color: #555;">Email:</td>
                    <td style="padding: 8px;">{booking.customer_email}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold; color: #555;">Phone:</td>
                    <td style="padding: 8px;">{booking.customer_phone or 'N/A'}</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="padding: 8px; font-weight: bold; color: #555;">Language:</td>
                    <td style="padding: 8px;">{booking.language.upper()}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold; color: #555;">Message:</td>
                    <td style="padding: 8px;">{booking.message or 'No additional message'}</td>
                </tr>
            </table>

            <div style="text-align: center; margin-top: 20px;">
                <a href="{tour_url}" style="display: inline-block; padding: 12px 28px; background-color: #3498db; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px;">
                    🔗 View Tour on Website
                </a>
            </div>

            <p style="color: #888; font-size: 12px; margin-top: 20px; text-align: center;">
                This notification was sent automatically by the Travel Agency booking system.
            </p>
        </div>
    </body>
    </html>
    """


def _send_email(to_email: str, subject: str, html_body: str) -> None:
    """
    Send an email via SMTP.
    Uses TLS for security. Credentials are loaded from app settings.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM_EMAIL
    msg["To"] = to_email

    # Attach HTML body
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM_EMAIL, to_email, msg.as_string())
        logger.info(f"Email sent successfully to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        raise


@celery_app.task(
    bind=True,
    name="send_booking_notification",
    max_retries=3,
    default_retry_delay=60,  # Retry after 60 seconds
)
def send_booking_notification(self, booking_id: int) -> dict:
    """
    Celery task: Smart email routing for booking notifications.

    Flow:
    1. Load the booking from PostgreSQL.
    2. Look up the LanguageOperatorConfig matching booking.language.
    3. Send email to the language-specific operator.
    4. Send email to the agency director.

    Retries up to 3 times on failure with 60-second delay.
    """
    logger.info(f"Processing email notification for booking #{booking_id}")

    try:
        with Session(sync_engine) as db:
            # ── Load booking ─────────────────────────────────────
            booking = db.execute(
                select(Booking).where(Booking.id == booking_id)
            ).scalar_one_or_none()

            if not booking:
                logger.error(f"Booking #{booking_id} not found in database")
                return {"status": "error", "message": "Booking not found"}

            # ── Load associated tour ─────────────────────────────
            tour = db.execute(
                select(TourPackage).where(TourPackage.id == booking.tour_id)
            ).scalar_one_or_none()

            if not tour:
                logger.error(f"Tour #{booking.tour_id} not found for booking #{booking_id}")
                return {"status": "error", "message": "Tour not found"}

            # ── Look up language-specific operator ───────────────
            operator_config = db.execute(
                select(LanguageOperatorConfig).where(
                    LanguageOperatorConfig.language_code == booking.language,
                    LanguageOperatorConfig.is_active == True,
                )
            ).scalar_one_or_none()

            # ── Build email content ──────────────────────────────
            email_html = _build_email_html(booking, tour)
            subject = f"New Booking #{booking.id} — {tour.title_en} ({booking.language.upper()})"
            recipients_notified = []

            # ── Send to language-specific operator ───────────────
            if operator_config:
                try:
                    _send_email(operator_config.operator_email, subject, email_html)
                    recipients_notified.append(operator_config.operator_email)
                    logger.info(
                        f"Notification sent to {booking.language.upper()} operator: "
                        f"{operator_config.operator_name} ({operator_config.operator_email})"
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to email {booking.language.upper()} operator: {e}"
                    )
            else:
                logger.warning(
                    f"No active operator configured for language '{booking.language}'. "
                    f"Skipping operator notification."
                )

            # ── Always send to the agency director ───────────────
            try:
                _send_email(settings.DIRECTOR_EMAIL, subject, email_html)
                recipients_notified.append(settings.DIRECTOR_EMAIL)
                logger.info(f"Notification sent to director: {settings.DIRECTOR_EMAIL}")
            except Exception as e:
                logger.error(f"Failed to email director: {e}")

            return {
                "status": "success",
                "booking_id": booking_id,
                "language": booking.language,
                "recipients": recipients_notified,
            }

    except Exception as exc:
        logger.error(f"Email notification task failed for booking #{booking_id}: {exc}")
        # Retry with exponential backoff
        raise self.retry(exc=exc)
