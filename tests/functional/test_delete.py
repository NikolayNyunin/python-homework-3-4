from src.links.models import Link

import pytest
from httpx import AsyncClient

from http import HTTPStatus


class TestDelete:
    @pytest.mark.asyncio
    async def test_delete_not_found(self, client: AsyncClient):
        response = await client.delete('/links/test')

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Link with short code test does not exist'}

    @pytest.mark.asyncio
    async def test_delete_forbidden(self, client: AsyncClient, test_link3: Link):
        response = await client.delete(f'/links/{test_link3.short_code}')

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == {
            'detail': f'You do not have the rights to delete the link with short code {test_link3.short_code}'
        }

    @pytest.mark.asyncio
    async def test_delete_success(self, client: AsyncClient, test_link1: Link):
        response = await client.delete(f'/links/{test_link1.short_code}')

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'info': f'Link with short code {test_link1.short_code} was deleted successfully'}
