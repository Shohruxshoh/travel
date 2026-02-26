"""
FastAPI Application Entrypoint
------------------------------
Configures CORS, registers all routers, and provides
health check + database initialization endpoints.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import os

from app.config import get_settings
from app.database import engine, Base
from app.routers import tours, services, hotels, blog, gallery, bookings, admin, auth, upload

# ── Logging setup ────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)
settings = get_settings()


# ── Lifespan: create tables on startup ───────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler:
    - On startup: create all database tables if they don't exist.
    - On shutdown: dispose of the engine connection pool.
    """
    logger.info("Starting Travel Agency API...")
    async with engine.begin() as conn:
        # Import all models so Base.metadata is populated
        import app.models  # noqa: F401
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables verified/created.")
    yield
    await engine.dispose()
    logger.info("Travel Agency API shut down.")


# ── FastAPI app instance ─────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Professional multilingual travel agency API supporting "
        "Russian (RU), English (EN), and French (FR). "
        "Features smart email routing for booking notifications."
    ),
    lifespan=lifespan,
)

# ── CORS middleware ──────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register all routers ────────────────────────────────────────
app.include_router(auth.router, prefix="/api")
app.include_router(tours.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(hotels.router, prefix="/api")
app.include_router(blog.router, prefix="/api")
app.include_router(gallery.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(upload.router, prefix="/api")

# ── Serve uploaded files ─────────────────────────────────────────
upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(upload_dir, exist_ok=True)
app.mount("/api/uploads", StaticFiles(directory=upload_dir), name="uploads")


# ── Health check ─────────────────────────────────────────────────
@app.get("/api/health", tags=["Health"])
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
