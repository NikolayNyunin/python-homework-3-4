import pytest
from httpx import AsyncClient

from http import HTTPStatus
import re


class TestCreate:
    @pytest.mark.asyncio
    async def test_create_success_random(self, client: AsyncClient):
        json_data = {'url': 'https://example.com/'}

        response = await client.post('/links/shorten', json=json_data)

        assert response.status_code == HTTPStatus.CREATED
        response_data = response.json()
        assert type(response_data) == dict
        assert bool(re.fullmatch(r'Link with short code \w+ was created successfully',
                                 response_data['info'])) is True

        short_code = response_data['info'].split()[4]
        await client.delete(f'/links/{short_code}')

    @pytest.mark.asyncio
    async def test_create_success_custom(self, client: AsyncClient):
        json_data = {
            'url': 'https://example.com/',
            'custom_alias': 'test'
        }

        response = await client.post('/links/shorten', json=json_data)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {'info': 'Link with short code test was created successfully'}

    @pytest.mark.asyncio
    async def test_create_success_custom_and_date(self, client: AsyncClient):
        json_data = {
            'url': 'https://example.com/',
            'custom_alias': 'test1',
            'expires_at': '2030-01-01T00:00:00+00:00'
        }

        response = await client.post('/links/shorten', json=json_data)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {'info': 'Link with short code test1 was created successfully'}

        await client.delete(f'/links/test1')

    @pytest.mark.asyncio
    async def test_create_conflict(self, client: AsyncClient):
        json_data = {
            'url': 'https://example.com/',
            'custom_alias': 'test'
        }

        response = await client.post('/links/shorten', json=json_data)

        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json() == {'detail': 'Custom alias is already taken'}

        await client.delete(f'/links/test')

    @pytest.mark.asyncio
    async def test_create_alias_invalid(self, client: AsyncClient):
        json_data = {
            'url': 'https://example.com/',
            'custom_alias': 'тест'
        }

        response = await client.post('/links/shorten', json=json_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json() == {'detail': 'Custom alias must consist of 3 to 10 latin letters or numbers'}

    @pytest.mark.asyncio
    async def test_create_alias_past_date(self, client: AsyncClient):
        json_data = {
            'url': 'https://example.com/',
            'expires_at': '2020-01-01T00:00:00+00:00'
        }

        response = await client.post('/links/shorten', json=json_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json() == {'detail': 'Expiration time must be in the future'}
