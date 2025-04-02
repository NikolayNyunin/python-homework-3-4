from src.links.models import Link

import pytest
from httpx import AsyncClient

from http import HTTPStatus


class TestRedirect:
    @pytest.mark.asyncio
    async def test_redirect_not_found(self, client: AsyncClient):
        response = await client.get(f'/links/test')

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Link with short code test does not exist'}

    @pytest.mark.asyncio
    async def test_redirect_found(self, client: AsyncClient, test_link1: Link):
        response = await client.get(f'/links/{test_link1.short_code}')

        assert response.status_code == HTTPStatus.PERMANENT_REDIRECT
        assert response.headers['location'] == test_link1.original_url
