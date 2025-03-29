from src.database import get_async_session
from src.auth.database import User
from src.auth.users import current_active_user
from src.links.schemas import CreateRequest, UpdateRequest, APIResponse, StatsResponse, SearchResponse
from src.links.models import Link
from src.links.utils import validate_short_code, is_free, generate_short_code

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from pydantic import HttpUrl

from http import HTTPStatus
from datetime import datetime, timezone
from typing import List

router = APIRouter(prefix='/links', tags=['links'])


@router.post('/shorten', response_model=APIResponse, status_code=HTTPStatus.CREATED)
async def create(request: CreateRequest,
                 session: AsyncSession = Depends(get_async_session),
                 user: User = Depends(current_active_user)):
    """Создание короткой ссылки."""

    try:
        # Если передан кастомный идентификатор ссылки
        if request.custom_alias is not None:
            # Проверка валидности идентификатора
            if not validate_short_code(request.custom_alias):
                raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                                    detail='Custom alias must consist of 3 to 10 latin letters or numbers')
            # Проверка, что идентификатор не занят
            if not await is_free(request.custom_alias, session):
                raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                                    detail='Custom alias is already taken')
            short_code = request.custom_alias
        else:
            short_code = await generate_short_code(session)

        # Если передана дата истечения ссылки, проверка её валидности
        if request.expires_at is not None and request.expires_at <= datetime.now(timezone.utc):
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                                detail='Expiration time must be in the future')

        statement = insert(Link).values(user_id=user.id, short_code=short_code,
                                        original_url=str(request.url), expires_at=request.expires_at)
        await session.execute(statement)
        await session.commit()
        return {'info': f'Link with short code {short_code} was created successfully'}

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/search', response_model=List[SearchResponse])
async def search(original_url: HttpUrl, session: AsyncSession = Depends(get_async_session)):
    """Поиск короткой ссылки по оригинальному URL."""

    try:
        query = select(Link).where(Link.original_url == str(original_url))
        result = await session.execute(query)
        links = result.scalars().all()

        search_results = []
        for link in links:
            search_results.append({
                'short_code': link.short_code,
                'original_url': link.original_url,
                'created_at': link.created_at,
                'expires_at': link.expires_at
            })
        return search_results

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/{short_code}', status_code=HTTPStatus.PERMANENT_REDIRECT)
async def redirect(short_code: str, session: AsyncSession = Depends(get_async_session)):
    """Использование короткой ссылки (перенаправление по оригинальному URL)."""

    try:
        query = select(Link).where(Link.short_code == short_code)
        result = await session.execute(query)
        link = result.scalar_one()
        return RedirectResponse(url=link.original_url, status_code=HTTPStatus.PERMANENT_REDIRECT)

    except NoResultFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=f'Link with short code {short_code} does not exist')

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/{short_code}/stats', response_model=StatsResponse)
async def get_stats(short_code: str,
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_active_user)):
    """Получение статистики использования короткой ссылки."""

    raise NotImplementedError
    # TODO: implement


@router.put('/{short_code}', response_model=APIResponse)
async def update(short_code: str,
                 request: UpdateRequest,
                 session: AsyncSession = Depends(get_async_session),
                 user: User = Depends(current_active_user)):
    """Обновление короткой ссылки."""

    try:
        query = select(Link).where(Link.short_code == short_code)
        result = await session.execute(query)
        link = result.scalar_one()

        if link.user_id != user.id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                                detail=f'You do not have the rights to update the link with short code {short_code}')

        # Если передана дата истечения ссылки
        if request.expires_at is not None:
            # При передаче False удаляем время истечения ссылки
            if not request.expires_at:
                link.expires_at = None
            # При передаче даты проверяем её на валидность и обновляем
            elif isinstance(request.expires_at, datetime):
                if request.expires_at <= datetime.now(timezone.utc):
                    raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                                        detail='Expiration time must be in the future')
                link.expires_at = request.expires_at
            # Иначе возвращаем ошибку
            else:
                raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                                    detail='Field expires_at must be a datetime, False or None')

        link.original_url = str(request.new_url)
        await session.commit()
        return {'info': f'Link with short code {short_code} was updated successfully'}

    except NoResultFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=f'Link with short code {short_code} does not exist')

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete('/{short_code}', response_model=APIResponse)
async def delete(short_code: str,
                 session: AsyncSession = Depends(get_async_session),
                 user: User = Depends(current_active_user)):
    """Удаление короткой ссылки."""

    try:
        query = select(Link).where(Link.short_code == short_code)
        result = await session.execute(query)
        link = result.scalar_one()

        if link.user_id != user.id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                                detail=f'You do not have the rights to delete the link with short code {short_code}')

        await session.delete(link)
        await session.commit()
        return {'info': f'Link with short code {short_code} was deleted successfully'}

    except NoResultFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=f'Link with short code {short_code} does not exist')

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
