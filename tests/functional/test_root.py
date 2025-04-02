import pytest
from httpx import AsyncClient

from http import HTTPStatus


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    """Тест получения основной информации о приложении."""

    response = await client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'info': 'API для создания коротких ссылок', 'status': 'OK'}
