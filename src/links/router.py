from src.database import get_async_session
from src.links.schemas import CreateRequest, UpdateRequest, APIResponse, StatsResponse, SearchResponse
from src.links.models import Link

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from http import HTTPStatus
from typing import List

router = APIRouter(prefix='/links', tags=['links'])


@router.post('/shorten', response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create(request: CreateRequest, session: AsyncSession = Depends(get_async_session)):
    """Создание короткой ссылки."""

    pass


@router.get('/{short_code}')
async def redirect(short_code: str, session: AsyncSession = Depends(get_async_session)):
    """Использование короткой ссылки (перенаправление по оригинальному URL)."""

    try:
        query = select(Link).where(Link.short_code == short_code)
        result = await session.execute(query)
        link = result.scalar_one_or_none()
        if link:
            return RedirectResponse(url=link.original_url)
        return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Short code {short_code} not found')

    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.put('/{short_code}', response_model=APIResponse)
async def update(short_code: str, request: UpdateRequest, session: AsyncSession = Depends(get_async_session)):
    """Обновление короткой ссылки."""

    pass


@router.delete('/{short_code}', response_model=APIResponse)
async def delete(short_code: str, session: AsyncSession = Depends(get_async_session)):
    """Удаление короткой ссылки."""

    pass


@router.get('/{short_code}/stats', response_model=StatsResponse)
async def get_stats(short_link: str, session: AsyncSession = Depends(get_async_session)):
    """Получение статистики использования короткой ссылки."""

    pass


@router.get('/search', response_model=List[SearchResponse])
async def search(original_url: str, session: AsyncSession = Depends(get_async_session)):
    """Поиск короткой ссылки по оригинальному URL."""

    pass
