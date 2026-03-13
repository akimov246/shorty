from fastapi import FastAPI, Request, Body, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, PlainTextResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.crud.urls import create_map, get_url
from typing import Annotated
import uvicorn

app = FastAPI(
    title="Shorty",
    redoc_url=None,
    description="API to shorten URLs and generate short links"
)

@app.post("/original_url",
          response_model=str,
          response_class=PlainTextResponse,
          status_code=status.HTTP_201_CREATED
)
async def original_url(
        request: Request,
        url: Annotated[str, Body(min_length=1)],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> str:
    base_url = str(request.base_url)
    print(request.body())
    short_code = await create_map(url, session)
    short_url = base_url + short_code
    return short_url

@app.get("/{short_code}")
async def shorten_url(
        short_code: str,
        session: Annotated[AsyncSession, Depends(get_session)]
) -> RedirectResponse:
    url = await get_url(short_code, session)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shorten URL not found")
    return RedirectResponse(url=url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000)