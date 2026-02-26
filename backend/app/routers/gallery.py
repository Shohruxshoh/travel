"""
Gallery API Router
------------------
Endpoints for listing gallery media items.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models.gallery import GalleryItem
from app.schemas.gallery import GalleryResponse

router = APIRouter(prefix="/gallery", tags=["Gallery"])


@router.get("/", response_model=list[GalleryResponse])
async def list_gallery(
    media_type: Optional[str] = Query(None, pattern="^(image|video)$"),
    tour_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """
    List gallery items with optional filters:
    - media_type: 'image' or 'video'
    - tour_id: filter by associated tour
    """
    query = select(GalleryItem)
    if media_type:
        query = query.where(GalleryItem.media_type == media_type)
    if tour_id:
        query = query.where(GalleryItem.tour_id == tour_id)
    query = query.order_by(GalleryItem.sort_order, GalleryItem.id).offset(offset).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()
