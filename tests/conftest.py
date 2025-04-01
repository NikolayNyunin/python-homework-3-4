from src.main import app, cleanup_expired_links
from src.database import get_async_session
from src.auth.users import current_active_user, User
from src.links.models import Link, Redirect
from src.auth.database import Base as AuthBase
from src.links.models import Base as LinksBase

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

import uuid
from datetime import datetime, timezone

# Создаем тестовую базу данных (SQLite in-memory)
TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest_asyncio.fixture(scope='session')
async def session():
    FastAPICache.init(InMemoryBackend(), prefix='test-cache')
    async with engine.begin() as connection:
        await connection.run_sync(AuthBase.metadata.create_all)
        await connection.run_sync(LinksBase.metadata.create_all)
    async with test_session_maker() as session:
        yield session
    async with engine.begin() as connection:
        await connection.run_sync(AuthBase.metadata.drop_all)
        await connection.run_sync(LinksBase.metadata.drop_all)


@pytest_asyncio.fixture(scope='function')
async def client(session, mocker):
    async def override_get_async_session():
        yield session

    app.dependency_overrides[get_async_session] = override_get_async_session

    def override_current_active_user():
        return User(id=uuid.uuid4(), email='test@example.com', hashed_password='PASSWORD')

    app.dependency_overrides[current_active_user] = override_current_active_user

    async def mock_cleanup(_):
        return await cleanup_expired_links(session)

    mocker.patch('src.main.cleanup_expired_links', new=mock_cleanup)

    yield TestClient(app)


@pytest_asyncio.fixture
async def test_user(session):
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        hashed_password="fakehashedpass",
        is_active=True,
        is_verified=True,
        is_superuser=False,
    )
    session.add(user)
    await session.commit()
    return user


@pytest_asyncio.fixture
async def test_link(session, test_user):
    link = Link(
        short_code="test123",
        original_url="https://example.com",
        user_id=test_user.id,
    )
    session.add(link)
    await session.commit()
    return link


@pytest_asyncio.fixture
async def test_redirect(session, test_link):
    redirect = Redirect(
        link_id=test_link.id,
        timestamp=datetime.now(timezone.utc),
    )
    session.add(redirect)
    await session.commit()
    return redirect
