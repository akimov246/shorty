from fastapi import FastAPI, Request, Body, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, PlainTextResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from app.redis_init import redis_client, RedisRateLimiter
from app.config import settings

from app.database import get_session, engine
from app.crud.urls import create_map, get_url
from typing import Annotated
from app.admin_panel import UrlAdmin
from sqladmin import Admin
import uvicorn

app = FastAPI(
    title="Shorty",
    redoc_url=None,
    description="API to shorten URLs and generate short links"
)

admin = Admin(app, engine)
admin.add_view(UrlAdmin)

redis_rate_limiter = RedisRateLimiter()

@app.post("/original_url",
          response_model=str,
          response_class=PlainTextResponse,
          status_code=status.HTTP_201_CREATED,
          dependencies=[Depends(redis_rate_limiter)]
)
async def original_url(
        request: Request,
        url: Annotated[str, Body(min_length=1, max_length=4096)],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> str:
    base_url = str(request.base_url)
    short_code = await create_map(url, session)
    await redis_client.set(short_code, url, ex=settings.REDIS_EXPIRE_SECONDS)
    short_url = base_url + short_code
    return short_url

@app.get("/{short_code}")
async def shorten_url(
        short_code: str,
        session: Annotated[AsyncSession, Depends(get_session)]
) -> RedirectResponse:
    if short_code == "admin":
        return RedirectResponse(url="/admin/")

    cached_url = await redis_client.get(short_code)
    if cached_url is not None:
        return RedirectResponse(url=cached_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    url = await get_url(short_code, session)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shorten URL not found")
    await redis_client.set(short_code, url, ex=settings.REDIS_EXPIRE_SECONDS)
    return RedirectResponse(url=url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000)