from app.models.url import Url
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.utils.short_code import generate_short_code

async def create_map(url: str, session: AsyncSession) -> str:
    map = Url(
        short_code="temp",
        url=url
    )
    session.add(map)
    await session.flush()
    map.short_code = generate_short_code(map.id)
    await session.commit()
    await session.refresh(map)
    return map.short_code

async def get_url(short_code: str, session: AsyncSession) -> str | None:
    row = await session.exec(
        select(Url)
        .where(Url.short_code == short_code)
    )
    result = row.one_or_none()
    if not result:
        return None
    return result.url