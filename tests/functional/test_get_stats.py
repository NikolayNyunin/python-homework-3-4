import asyncio

from src.links.models import Link

import pytest
from httpx import AsyncClient

from http import HTTPStatus


class TestGetStats:
    @pytest.mark.asyncio
    async def test_get_stats_not_found(self, client: AsyncClient):
        response = await client.get('/links/test/stats')

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Link with short code test does not exist'}

    @pytest.mark.asyncio
    async def test_get_stats_forbidden(self, client: AsyncClient, test_link3: Link):
        response = await client.get(f'/links/{test_link3.short_code}/stats')

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == {
            'detail': f'You do not have the rights to view stats for the link with short code {test_link3.short_code}'
        }

    @pytest.mark.asyncio
    async def test_get_stats_default(self, client: AsyncClient, test_link1: Link):
        response = await client.get(f'/links/{test_link1.short_code}/stats')

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            'short_code': test_link1.short_code,
            'original_url': test_link1.original_url,
            'created_at': test_link1.created_at.isoformat(),
            'expires_at': test_link1.expires_at.isoformat(),
            'redirect_count': 0,
            'latest_redirect_at': None
        }

    @pytest.mark.asyncio
    async def test_get_stats_modified(self, client: AsyncClient, test_link1: Link, session):
        await client.get(f'/links/{test_link1.short_code}')

        response1 = await client.get(f'/links/{test_link1.short_code}/stats')

        assert response1.status_code == HTTPStatus.OK
        response_data1 = response1.json()
        assert type(response_data1) == dict
        assert response_data1['short_code'] == test_link1.short_code
        assert response_data1['original_url'] == test_link1.original_url
        assert response_data1['created_at'] == test_link1.created_at.isoformat()
        assert response_data1['expires_at'] == test_link1.expires_at.isoformat()
        assert response_data1['redirect_count'] == 1

        await asyncio.sleep(1)

        await client.get(f'/links/{test_link1.short_code}')

        response2 = await client.get(f'/links/{test_link1.short_code}/stats')

        assert response2.status_code == HTTPStatus.OK
        response_data2 = response2.json()
        assert type(response_data2) == dict
        assert response_data2['short_code'] == test_link1.short_code
        assert response_data2['original_url'] == test_link1.original_url
        assert response_data2['created_at'] == test_link1.created_at.isoformat()
        assert response_data2['expires_at'] == test_link1.expires_at.isoformat()
        assert response_data2['redirect_count'] == 2
        assert response_data1['latest_redirect_at'] != response_data2['latest_redirect_at']
