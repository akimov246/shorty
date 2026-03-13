from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

engine = create_async_engine(settings.POSTGRES_URL)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session