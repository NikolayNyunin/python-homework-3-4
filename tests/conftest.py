from sqlalchemy import delete

from src.main import app
from src.database import get_async_session
from src.auth.users import current_active_user, User
from src.links.models import Link
from src.auth.database import Base as AuthBase
from src.links.models import Base as LinksBase

import pytest
import pytest_mock
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional

# Создаем тестовую базу данных (SQLite in-memory)
TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'
engine = create_async_engine(TEST_DATABASE_URL, connect_args={'check_same_thread': False}, echo=False)
test_session_maker = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


class SafeInMemoryBackend(InMemoryBackend):
    async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
        count = 0
        if namespace:
            keys = list(self._store.keys())
            for key in keys:
                if key.startswith(namespace):
                    del self._store[key]
                    count += 1
        elif key and key in self._store:
            del self._store[key]
            count += 1
        return count


@pytest.fixture(scope='session', autouse=True)
async def setup():
    FastAPICache.init(SafeInMemoryBackend(), prefix='fastapi-cache')
    async with engine.begin() as connection:
        await connection.run_sync(AuthBase.metadata.create_all)
        await connection.run_sync(LinksBase.metadata.create_all)
    yield
    await FastAPICache.clear()
    async with engine.begin() as connection:
        await connection.run_sync(AuthBase.metadata.drop_all)
        await connection.run_sync(LinksBase.metadata.drop_all)


@pytest.fixture
async def session():
    async with test_session_maker() as session:
        yield session


@pytest.fixture
async def client(session: AsyncSession, mocker: pytest_mock.mocker):
    async def override_get_async_session():
        async with test_session_maker() as s:
            yield s

    app.dependency_overrides[get_async_session] = override_get_async_session

    def override_current_active_user():
        return User(
            id=uuid.UUID('123e4567-e89b-12d3-a456-426614174000'),
            email='test@example.com',
            hashed_password='password',
            is_active=True,
            is_verified=True,
            is_superuser=False
        )

    app.dependency_overrides[current_active_user] = override_current_active_user

    async def mock_cleanup(_):
        async with test_session_maker() as s:
            await s.execute(delete(Link).where(Link.expires_at <= datetime.now(timezone.utc).replace(tzinfo=None)))
            await s.commit()

    mocker.patch('src.main.cleanup_expired_links', new=mock_cleanup)

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def test_link1(session):
    async with session.begin():
        link = Link(
            short_code='test1',
            original_url='https://example.com/',
            user_id=uuid.UUID('123e4567-e89b-12d3-a456-426614174000'),
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(days=1)
        )

        session.add(link)
        await session.flush()
        await session.refresh(link)

        link_data = {
            'id': link.id,
            'short_code': link.short_code,
            'original_url': link.original_url,
            'user_id': link.user_id,
            'created_at': link.created_at,
            'expires_at': link.expires_at
        }

        await session.commit()

    link_copy = Link(**link_data)

    yield link_copy

    async with session.begin():
        await session.delete(await session.get(Link, link_copy.id))
        await session.commit()


@pytest.fixture
async def test_link2(session):
    async with session.begin():
        link = Link(
            short_code='test2',
            original_url='https://example.com/',
            user_id=uuid.UUID('123e4567-e89b-12d3-a456-426614174000'),
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(days=1)
        )

        session.add(link)
        await session.flush()
        await session.refresh(link)

        link_data = {
            'id': link.id,
            'short_code': link.short_code,
            'original_url': link.original_url,
            'user_id': link.user_id,
            'created_at': link.created_at,
            'expires_at': link.expires_at
        }

        await session.commit()

    link_copy = Link(**link_data)

    yield link_copy

    async with session.begin():
        await session.delete(await session.get(Link, link_copy.id))
        await session.commit()


@pytest.fixture
async def test_link3(session):
    async with session.begin():
        link = Link(
            short_code='test3',
            original_url='https://example.com/',
            user_id=uuid.uuid4(),
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(days=1)
        )

        session.add(link)
        await session.flush()
        await session.refresh(link)

        link_data = {
            'id': link.id,
            'short_code': link.short_code,
            'original_url': link.original_url,
            'user_id': link.user_id,
            'created_at': link.created_at,
            'expires_at': link.expires_at
        }

        await session.commit()

    link_copy = Link(**link_data)

    yield link_copy

    async with session.begin():
        await session.delete(await session.get(Link, link_copy.id))
        await session.commit()
