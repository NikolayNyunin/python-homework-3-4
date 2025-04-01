from fastapi.testclient import TestClient

from http import HTTPStatus


def test_root(client: TestClient):
    """Тест получения основной информации о приложении."""

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'info': 'API для создания коротких ссылок', 'status': 'OK'}
