from src.links.models import Link

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from string import ascii_letters, digits
from random import choices


def validate_short_code(short_code: str) -> bool:
    """Проверка валидности идентификатора короткой ссылки."""

    if len(short_code) < 3 or len(short_code) > 10:
        return False

    valid_characters = ascii_letters + digits
    for char in short_code:
        if char not in valid_characters:
            return False

    return True


async def is_free(short_code: str, session: AsyncSession) -> bool:
    """Проверка, свободен ли идентификатор короткой ссылки."""

    query = select(Link).where(Link.short_code == short_code)
    result = await session.execute(query)
    if result.scalar_one_or_none():
        return False
    return True


async def generate_short_code(session: AsyncSession) -> str:
    """Генерация идентификатора короткой ссылки с проверкой на уникальность."""

    valid_characters = ascii_letters + digits

    short_code = ''.join(choices(valid_characters, k=8))
    while not await is_free(short_code, session):
        short_code = ''.join(choices(valid_characters, k=8))

    return short_code
