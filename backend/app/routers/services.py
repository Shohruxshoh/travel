"""
Services API Router
-------------------
Endpoints for listing and retrieving agency services.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.service import Service
from app.schemas.service import ServiceResponse

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/", response_model=list[ServiceResponse])
async def list_services(
    active_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    """List all available agency services."""
    query = select(Service)
    if active_only:
        query = query.where(Service.is_active == True)
    query = query.order_by(Service.id)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a specific service by ID."""
    result = await db.execute(
        select(Service).where(Service.id == service_id)
    )
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service
