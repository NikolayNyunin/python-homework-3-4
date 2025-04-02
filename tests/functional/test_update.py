from src.links.models import Link

import pytest
from httpx import AsyncClient

from http import HTTPStatus


class TestUpdate:
    @pytest.mark.asyncio
    async def test_update_not_found(self, client: AsyncClient):
        json_data = {'new_url': 'https://example.com/'}

        response = await client.put('/links/test', json=json_data)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Link with short code test does not exist'}

    @pytest.mark.asyncio
    async def test_update_forbidden(self, client: AsyncClient, test_link3: Link):
        json_data = {'new_url': 'https://example.com/'}

        response = await client.put(f'/links/{test_link3.short_code}', json=json_data)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == {
            'detail': f'You do not have the rights to update the link with short code {test_link3.short_code}'
        }

    @pytest.mark.asyncio
    async def test_update_success_no_date(self, client: AsyncClient, test_link1: Link):
        json_data = {'new_url': 'https://example.com/'}

        response = await client.put(f'/links/{test_link1.short_code}', json=json_data)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'info': f'Link with short code {test_link1.short_code} was updated successfully'}

    @pytest.mark.asyncio
    async def test_update_success_date_false(self, client: AsyncClient, test_link1: Link):
        json_data = {
            'new_url': 'https://example.com/',
            'expires_at': False
        }

        stats1 = await client.get(f'/links/{test_link1.short_code}/stats')
        assert stats1.json()['expires_at'] is not None

        response = await client.put(f'/links/{test_link1.short_code}', json=json_data)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'info': f'Link with short code {test_link1.short_code} was updated successfully'}

        stats2 = await client.get(f'/links/{test_link1.short_code}/stats')
        assert stats2.json()['expires_at'] is None

    @pytest.mark.asyncio
    async def test_update_failure_date_true(self, client: AsyncClient, test_link1: Link):
        json_data = {
            'new_url': 'https://example.com/',
            'expires_at': True
        }

        response = await client.put(f'/links/{test_link1.short_code}', json=json_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json() == {'detail': 'Field expires_at must be a datetime, False or None'}

    @pytest.mark.asyncio
    async def test_update_failure_past_date(self, client: AsyncClient, test_link1: Link):
        json_data = {
            'new_url': 'https://example.com/',
            'expires_at': '2020-01-01T00:00:00+00:00'
        }

        response = await client.put(f'/links/{test_link1.short_code}', json=json_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json() == {'detail': 'Expiration time must be in the future'}
