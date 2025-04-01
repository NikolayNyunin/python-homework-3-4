from locust import HttpUser, task, between

import random
import string
from http import HTTPStatus


class APIUser(HttpUser):
    wait_time = between(1, 3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.email = None
        self.password = None
        self.token = None
        self.short_code = None

    @staticmethod
    def random_string(length=8):
        """Генерация случайной строки."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def random_email(self):
        """Генерация случайного email."""
        return f'{self.random_string()}@example.com'

    def random_url(self):
        """Генерация случайного URL."""
        return f'https://example.com/{self.random_string()}'

    def on_start(self):
        """Стартовый метод."""

        # Регистрация и логин при старте пользователя
        self.email = self.random_email()
        self.password = 'testpassword123'

        # Регистрация
        register_data = {
            'email': self.email,
            'password': self.password,
            'is_active': True,
            'is_superuser': False,
            'is_verified': False
        }
        self.client.post('/auth/register', json=register_data, headers=self.headers)

        # Логин и сохранение токена
        login_data = {
            'username': self.email,
            'password': self.password
        }
        response = self.client.post('/auth/jwt/login', data=login_data)
        if response.status_code == 200:
            self.token = response.json().get('access_token')
            self.headers['Authorization'] = f'Bearer {self.token}'

        # Создание одной ссылки для дальнейшего тестирования
        self.short_code = self.random_string()
        create_data = {
            'url': self.random_url(),
            'custom_alias': self.short_code
        }
        self.client.post('/links/shorten', json=create_data, headers=self.headers)

    @task(1)
    def get_root(self):
        """Запрос GET к /."""
        self.client.get('/')

    @task(2)
    def create_delete_link(self):
        """Запросы POST к /links/shorten и DELETE к /links/{short_code}."""
        short_code = self.random_string()
        data = {
            'url': self.random_url(),
            'custom_alias': short_code
        }
        self.client.post('/links/shorten', json=data, headers=self.headers)
        self.client.delete(f'/links/{short_code}', headers=self.headers)

    @task(5)
    def redirect(self):
        """Запрос GET к /links/{short_code}."""
        with self.client.get(f'/links/{self.short_code}', allow_redirects=False, catch_response=True) as response:
            if response.status_code == HTTPStatus.PERMANENT_REDIRECT:
                response.success()
            else:
                response.failure(f'Unexpected status: {response.status_code}')

    @task(2)
    def search_links(self):
        """Запрос GET к /links/search."""
        original_url = self.random_url()
        self.client.get(f'/links/search?original_url={original_url}')

    @task(2)
    def get_user_links(self):
        """Запрос GET к /links/user."""
        self.client.get('/links/user', headers=self.headers)

    @task(2)
    def get_link_stats(self):
        """Запрос GET к /links/{short_code}/stats."""
        self.client.get(f'/links/{self.short_code}/stats', headers=self.headers)

    @task(1)
    def update_link(self):
        """Запрос PUT к /links/{short_code}."""
        data = {'new_url': self.random_url()}
        self.client.put(f'/links/{self.short_code}', json=data, headers=self.headers)

    def on_stop(self):
        """Завершающий метод."""
        self.client.delete(f'/links/{self.short_code}', headers=self.headers)
        self.client.post('/auth/jwt/logout', headers=self.headers)
