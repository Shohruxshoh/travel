"""
Hotels API Router
-----------------
Endpoints for listing and retrieving hotel listings.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models.hotel import Hotel
from app.schemas.hotel import HotelResponse

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/", response_model=list[HotelResponse])
async def list_hotels(
    active_only: bool = Query(True),
    min_stars: Optional[int] = Query(None, ge=1, le=5),
    city: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """
    List hotels with optional filters by star rating and city.
    """
    query = select(Hotel)
    if active_only:
        query = query.where(Hotel.is_active == True)
    if min_stars:
        query = query.where(Hotel.star_rating >= min_stars)
    if city:
        query = query.where(Hotel.city.ilike(f"%{city}%"))
    query = query.order_by(Hotel.star_rating.desc()).offset(offset).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{hotel_id}", response_model=HotelResponse)
async def get_hotel(hotel_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a specific hotel by ID."""
    result = await db.execute(
        select(Hotel).where(Hotel.id == hotel_id)
    )
    hotel = result.scalar_one_or_none()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel
