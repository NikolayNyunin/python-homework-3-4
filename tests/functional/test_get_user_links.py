from src.links.models import Link

import pytest
from httpx import AsyncClient

from http import HTTPStatus
from datetime import datetime


class TestGetUserLinks:
    @pytest.mark.asyncio
    async def test_get_user_links_zero(self, client: AsyncClient):
        response = await client.get('/links/user')

        assert response.status_code == HTTPStatus.OK
        response_data = response.json()
        assert type(response_data) == list
        assert len(response_data) == 0

    @pytest.mark.asyncio
    async def test_get_user_links_one(self, client: AsyncClient, test_link1: Link):
        response = await client.get('/links/user')

        assert response.status_code == HTTPStatus.OK
        response_data = response.json()
        assert type(response_data) == list
        assert len(response_data) == 1
        assert response_data[0]['short_code'] == test_link1.short_code
        assert response_data[0]['original_url'] == test_link1.original_url
        assert datetime.fromisoformat(response_data[0]['created_at']) == test_link1.created_at
        assert datetime.fromisoformat(response_data[0]['expires_at']) == test_link1.expires_at

    @pytest.mark.asyncio
    async def test_get_user_links_two(self, client: AsyncClient, test_link1: Link, test_link2: Link):
        response = await client.get('/links/user')

        assert response.status_code == HTTPStatus.OK
        response_data = response.json()
        assert type(response_data) == list
        assert len(response_data) == 2
        if response_data[0]['short_code'] == test_link1.short_code:
            assert response_data[0]['short_code'] == test_link1.short_code
            assert response_data[0]['original_url'] == test_link1.original_url
            assert datetime.fromisoformat(response_data[0]['created_at']) == test_link1.created_at
            assert datetime.fromisoformat(response_data[0]['expires_at']) == test_link1.expires_at
            assert response_data[1]['short_code'] == test_link2.short_code
            assert response_data[1]['original_url'] == test_link2.original_url
            assert datetime.fromisoformat(response_data[1]['created_at']) == test_link2.created_at
            assert datetime.fromisoformat(response_data[1]['expires_at']) == test_link2.expires_at
        else:
            assert response_data[0]['short_code'] == test_link2.short_code
            assert response_data[0]['original_url'] == test_link2.original_url
            assert datetime.fromisoformat(response_data[0]['created_at']) == test_link2.created_at
            assert datetime.fromisoformat(response_data[0]['expires_at']) == test_link2.expires_at
            assert response_data[1]['short_code'] == test_link1.short_code
            assert response_data[1]['original_url'] == test_link1.original_url
            assert datetime.fromisoformat(response_data[1]['created_at']) == test_link1.created_at
            assert datetime.fromisoformat(response_data[1]['expires_at']) == test_link1.expires_at
