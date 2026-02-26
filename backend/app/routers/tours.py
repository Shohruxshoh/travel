"""
Tours API Router
----------------
Endpoints for listing and retrieving tour packages.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models.tour import TourPackage
from app.schemas.tour import TourResponse

router = APIRouter(prefix="/tours", tags=["Tours"])


@router.get("/", response_model=list[TourResponse])
async def list_tours(
    active_only: bool = Query(True, description="Filter by active status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """
    List all tour packages.
    Supports pagination and filtering by active status.
    """
    query = select(TourPackage)
    if active_only:
        query = query.where(TourPackage.is_active == True)
    query = query.order_by(TourPackage.created_at.desc()).offset(offset).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{tour_id}", response_model=TourResponse)
async def get_tour(tour_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a specific tour package by ID."""
    result = await db.execute(
        select(TourPackage).where(TourPackage.id == tour_id)
    )
    tour = result.scalar_one_or_none()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    return tour
