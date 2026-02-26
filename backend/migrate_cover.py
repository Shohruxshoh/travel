import asyncio
from app.database import engine
from sqlalchemy import text

async def migrate():
    async with engine.begin() as conn:
        await conn.execute(text("ALTER TABLE tour_packages ADD COLUMN IF NOT EXISTS cover_image VARCHAR(512)"))
        print("cover_image column added to tour_packages")

asyncio.run(migrate())
