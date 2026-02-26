"""
Admin CRUD Router
-----------------
Full CRUD endpoints for managing all entities through the admin panel.
All endpoints require JWT authentication via the require_admin dependency.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.auth import require_admin

# Models
from app.models.tour import TourPackage
from app.models.hotel import Hotel
from app.models.service import Service
from app.models.blog import BlogArticle
from app.models.booking import Booking
from app.models.operator_config import LanguageOperatorConfig
from app.models.gallery import GalleryItem

# Schemas
from app.schemas.tour import TourCreate, TourUpdate, TourResponse
from app.schemas.hotel import HotelCreate, HotelResponse
from app.schemas.service import ServiceCreate, ServiceResponse
from app.schemas.blog import BlogCreate, BlogResponse
from app.schemas.booking import (
    BookingResponse,
    OperatorConfigCreate,
    OperatorConfigUpdate,
    OperatorConfigResponse,
)
from app.schemas.gallery import GalleryCreate, GalleryResponse

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],
)


# ═══════════════════════════════════════════════════
# DASHBOARD STATS
# ═══════════════════════════════════════════════════
@router.get("/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Return counts for the admin dashboard."""
    tours_count = (await db.execute(select(func.count(TourPackage.id)))).scalar() or 0
    hotels_count = (await db.execute(select(func.count(Hotel.id)))).scalar() or 0
    bookings_count = (await db.execute(select(func.count(Booking.id)))).scalar() or 0
    services_count = (await db.execute(select(func.count(Service.id)))).scalar() or 0
    operators_count = (await db.execute(select(func.count(LanguageOperatorConfig.id)))).scalar() or 0
    blog_count = (await db.execute(select(func.count(BlogArticle.id)))).scalar() or 0
    gallery_count = (await db.execute(select(func.count(GalleryItem.id)))).scalar() or 0
    return {
        "tours": tours_count,
        "hotels": hotels_count,
        "bookings": bookings_count,
        "services": services_count,
        "operators": operators_count,
        "blog": blog_count,
        "gallery": gallery_count,
    }


# ═══════════════════════════════════════════════════
# TOURS CRUD
# ═══════════════════════════════════════════════════
@router.get("/tours", response_model=list[TourResponse])
async def admin_list_tours(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TourPackage).order_by(TourPackage.id.desc()))
    return result.scalars().all()


@router.post("/tours", response_model=TourResponse, status_code=201)
async def admin_create_tour(data: TourCreate, db: AsyncSession = Depends(get_db)):
    tour = TourPackage(**data.model_dump())
    db.add(tour)
    await db.flush()
    await db.refresh(tour)
    return tour


@router.put("/tours/{tour_id}", response_model=TourResponse)
async def admin_update_tour(tour_id: int, data: TourUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TourPackage).where(TourPackage.id == tour_id))
    tour = result.scalar_one_or_none()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(tour, field, value)
    await db.flush()
    await db.refresh(tour)
    return tour


@router.delete("/tours/{tour_id}", status_code=204)
async def admin_delete_tour(tour_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TourPackage).where(TourPackage.id == tour_id))
    tour = result.scalar_one_or_none()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    await db.delete(tour)


# ═══════════════════════════════════════════════════
# HOTELS CRUD
# ═══════════════════════════════════════════════════
@router.get("/hotels", response_model=list[HotelResponse])
async def admin_list_hotels(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hotel).order_by(Hotel.id.desc()))
    return result.scalars().all()


@router.post("/hotels", response_model=HotelResponse, status_code=201)
async def admin_create_hotel(data: HotelCreate, db: AsyncSession = Depends(get_db)):
    hotel = Hotel(**data.model_dump())
    db.add(hotel)
    await db.flush()
    await db.refresh(hotel)
    return hotel


@router.put("/hotels/{hotel_id}", response_model=HotelResponse)
async def admin_update_hotel(hotel_id: int, data: HotelCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
    hotel = result.scalar_one_or_none()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(hotel, field, value)
    await db.flush()
    await db.refresh(hotel)
    return hotel


@router.delete("/hotels/{hotel_id}", status_code=204)
async def admin_delete_hotel(hotel_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
    hotel = result.scalar_one_or_none()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    await db.delete(hotel)


# ═══════════════════════════════════════════════════
# SERVICES CRUD
# ═══════════════════════════════════════════════════
@router.get("/services", response_model=list[ServiceResponse])
async def admin_list_services(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).order_by(Service.id.desc()))
    return result.scalars().all()


@router.post("/services", response_model=ServiceResponse, status_code=201)
async def admin_create_service(data: ServiceCreate, db: AsyncSession = Depends(get_db)):
    service = Service(**data.model_dump())
    db.add(service)
    await db.flush()
    await db.refresh(service)
    return service


@router.put("/services/{service_id}", response_model=ServiceResponse)
async def admin_update_service(service_id: int, data: ServiceCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    await db.flush()
    await db.refresh(service)
    return service


@router.delete("/services/{service_id}", status_code=204)
async def admin_delete_service(service_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    await db.delete(service)


# ═══════════════════════════════════════════════════
# BLOG CRUD
# ═══════════════════════════════════════════════════
@router.get("/blog", response_model=list[BlogResponse])
async def admin_list_blog(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BlogArticle).order_by(BlogArticle.id.desc()))
    return result.scalars().all()


@router.post("/blog", response_model=BlogResponse, status_code=201)
async def admin_create_blog(data: BlogCreate, db: AsyncSession = Depends(get_db)):
    article = BlogArticle(**data.model_dump())
    db.add(article)
    await db.flush()
    await db.refresh(article)
    return article


@router.put("/blog/{article_id}", response_model=BlogResponse)
async def admin_update_blog(article_id: int, data: BlogCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BlogArticle).where(BlogArticle.id == article_id))
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(article, field, value)
    await db.flush()
    await db.refresh(article)
    return article


@router.delete("/blog/{article_id}", status_code=204)
async def admin_delete_blog(article_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BlogArticle).where(BlogArticle.id == article_id))
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    await db.delete(article)


# ═══════════════════════════════════════════════════
# BOOKINGS (read + update status + delete)
# ═══════════════════════════════════════════════════
@router.get("/bookings", response_model=list[BookingResponse])
async def admin_list_bookings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Booking).order_by(Booking.created_at.desc()).limit(200))
    return result.scalars().all()


@router.put("/bookings/{booking_id}")
async def admin_update_booking_status(
    booking_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if "status" in data:
        booking.status = data["status"]
    await db.flush()
    await db.refresh(booking)
    return {"id": booking.id, "status": booking.status}


@router.delete("/bookings/{booking_id}", status_code=204)
async def admin_delete_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    await db.delete(booking)


# ═══════════════════════════════════════════════════
# OPERATOR CONFIGS CRUD
# ═══════════════════════════════════════════════════
@router.get("/operator-configs", response_model=list[OperatorConfigResponse])
async def admin_list_operator_configs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(LanguageOperatorConfig).order_by(LanguageOperatorConfig.language_code)
    )
    return result.scalars().all()


@router.post("/operator-configs", response_model=OperatorConfigResponse, status_code=201)
async def admin_create_operator_config(data: OperatorConfigCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(LanguageOperatorConfig).where(
            LanguageOperatorConfig.language_code == data.language_code
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"Config for '{data.language_code}' already exists")
    config = LanguageOperatorConfig(**data.model_dump())
    db.add(config)
    await db.flush()
    await db.refresh(config)
    return config


@router.put("/operator-configs/{config_id}", response_model=OperatorConfigResponse)
async def admin_update_operator_config(
    config_id: int,
    data: OperatorConfigUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(LanguageOperatorConfig).where(LanguageOperatorConfig.id == config_id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="Operator config not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    await db.flush()
    await db.refresh(config)
    return config


@router.delete("/operator-configs/{config_id}", status_code=204)
async def admin_delete_operator_config(config_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(LanguageOperatorConfig).where(LanguageOperatorConfig.id == config_id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="Operator config not found")
    await db.delete(config)


# ═══════════════════════════════════════════════════════
# GALLERY CRUD
# ═══════════════════════════════════════════════════════
@router.get("/gallery", response_model=list[GalleryResponse])
async def admin_list_gallery(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GalleryItem).order_by(GalleryItem.sort_order, GalleryItem.id.desc()))
    return result.scalars().all()


@router.post("/gallery", response_model=GalleryResponse, status_code=201)
async def admin_create_gallery(data: GalleryCreate, db: AsyncSession = Depends(get_db)):
    item = GalleryItem(**data.model_dump())
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/gallery/{item_id}", response_model=GalleryResponse)
async def admin_update_gallery(item_id: int, data: GalleryCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GalleryItem).where(GalleryItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/gallery/{item_id}", status_code=204)
async def admin_delete_gallery(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GalleryItem).where(GalleryItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    await db.delete(item)
