"""
Comments API Router
-------------------
Public endpoints for reading and creating visitor comments/reviews.
No authentication required.
"""

import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(prefix="/comments", tags=["Comments"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
ALLOWED_IMG = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".avif", ".heic"}
MAX_IMG_SIZE = 5 * 1024 * 1024  # 5 MB

# Content-Type → extension fallback (when filename has no extension)
CONTENT_TYPE_MAP = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/bmp": ".bmp",
    "image/tiff": ".tiff",
    "image/avif": ".avif",
    "image/heic": ".heic",
}


@router.get("/", response_model=list[CommentResponse])
async def list_comments(
    tour_id: Optional[int] = Query(None, description="Filter by tour (omit for all comments)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """
    List all approved comments.
    Optionally filter by tour_id. Returns newest first.
    """
    query = select(Comment).where(Comment.approved == True)
    if tour_id is not None:
        query = query.where(Comment.tour_id == tour_id)
    query = query.order_by(Comment.created_at.desc()).offset(offset).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=CommentResponse, status_code=201)
async def create_comment(
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new public comment/review.
    No authentication required. Comments are approved by default.
    """
    comment = Comment(
        author_name=payload.author_name.strip(),
        country=payload.country.strip(),
        description=payload.description.strip(),
        tour_id=payload.tour_id,
        image_url=payload.image_url,
        approved=True,
    )
    db.add(comment)
    await db.flush()
    await db.refresh(comment)
    return comment


@router.post("/upload-image/")
async def upload_comment_image(file: UploadFile = File(...)):
    """Upload an image for a comment. Supports jpg, png, gif, webp, bmp, avif etc."""
    # Determine extension from filename first, then fall back to Content-Type
    ext = os.path.splitext(file.filename or "")[1].lower()
    if not ext and file.content_type:
        ext = CONTENT_TYPE_MAP.get(file.content_type.lower(), "")

    if ext not in ALLOWED_IMG:
        raise HTTPException(
            status_code=400,
            detail=f"Image type '{ext or file.content_type}' not allowed. "
                   f"Allowed: jpg, png, gif, webp, bmp, avif"
        )

    content = await file.read()
    if len(content) > MAX_IMG_SIZE:
        raise HTTPException(status_code=400, detail="Image too large. Max 5 MB.")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"comment_{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(content)

    return {"url": f"/api/uploads/{filename}", "filename": filename}
