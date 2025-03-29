from src.database import get_async_session
from src.links.router import router as links_router
from src.links.models import Link
from src.schemas import RootResponse
from src.auth.database import create_db_and_tables
from src.auth.users import auth_backend, fastapi_users
from src.auth.schemas import UserCreate, UserRead

from fastapi import FastAPI, Request
import uvicorn
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Callable


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(title='Link shortening API', lifespan=lifespan)

app.include_router(links_router)
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=['auth'])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix='/auth', tags=['auth'])


async def cleanup_expired_links(session: AsyncSession):
    """Удаление ссылок с истекшим сроком действия."""

    await session.execute(delete(Link).where(Link.expires_at <= datetime.now(timezone.utc)))
    await session.commit()


@app.middleware('http')
async def cleanup_middleware(request: Request, call_next: Callable):
    """Middleware для удаления устаревших ссылок."""

    # Асинхронное удаление устаревших ссылок
    async for session in get_async_session():
        await cleanup_expired_links(session)

    return await call_next(request)


@app.get('/', response_model=RootResponse)
async def root():
    """Получение основной информации о приложении."""

    return {'info': 'API для создания коротких ссылок', 'status': 'OK'}


if __name__ == '__main__':
    uvicorn.run('src.main:app', host='0.0.0.0', reload=True)
