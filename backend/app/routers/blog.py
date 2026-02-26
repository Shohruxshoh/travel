"""
Blog API Router
---------------
Endpoints for listing blog articles and retrieving by slug.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.blog import BlogArticle
from app.schemas.blog import BlogResponse

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.get("/", response_model=list[BlogResponse])
async def list_articles(
    published_only: bool = Query(True),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List blog articles, newest first."""
    query = select(BlogArticle)
    if published_only:
        query = query.where(BlogArticle.is_published == True)
    query = query.order_by(BlogArticle.published_at.desc()).offset(offset).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{slug}", response_model=BlogResponse)
async def get_article_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    """Retrieve a blog article by its URL slug."""
    result = await db.execute(
        select(BlogArticle).where(BlogArticle.slug == slug)
    )
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
