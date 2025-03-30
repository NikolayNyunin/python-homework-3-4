# Домашние задания №3,4 (Applied Python)

![Python](https://img.shields.io/badge/python-v3.12-blue.svg)

## Оглавление

- [Описание](#описание)
- [Структура проекта](#структура-проекта)
- [Запуск проекта](#запуск-проекта)
- [Методы API](#методы-api)

## Описание

Данный проект представляет собой FastAPI-сервис для создания коротких ссылок на внешние Интернет-ресурсы.

Функции работы с короткими ссылками:
- Создание ссылки по оригинальному URL (опционально с указанием желаемого короткого кода и времени жизни);
- Использование короткой ссылки (перенаправление на оригинальный URL);
- Изменение короткой ссылки (переназначение оригинального URL и времени жизни);
- Удаление короткой ссылки;
- Поиск коротких ссылок по оригинальному URL;
- Получение всех ссылок, созданных данным пользователем;
- Просмотр статистики использования короткой ссылки.

Основные технические особенности:
- Авторизация пользователей с использованием **fastapi-users**;
- Хранение данных о пользователях и ссылках с использованием СУБД **PostgreSQL** и **SQLAlchemy**;
- Описание миграций БД с использованием **Alembic**;
- Кэширование запросов с использованием **fastapi-cache2** и **Redis**;
- Контейнеризация с использованием **Docker Compose**;

Ссылка на развёрнутый сервис: ___
(используется бесплатный хостинг, так что сервер может отвечать медленно или не отвечать совсем).

## Структура проекта

- `task1.ipynb` — Jupyter-ноутбук с описанием требований к ДЗ 3;
- `README.md` — Markdown-файл с документацией приложения ***(данный файл)***;
- `src/` — модуль с кодом приложения;
  - `auth/` — модуль с кодом для аутентификации пользователей;
    - `database.py` — скрипт для работы с БД для хранения аккаунтов пользователей;
    - `users.py` — скрипт с конфигурацией системы аутентификации;
    - `schemas.py` — скрипт с описанием схем, связанных с аутентификацией;
  - `links/` — модуль с кодом для работы с короткими ссылками;
    - `router.py` — скрипт с описанием методов API для работы со ссылками;
    - `models.py` — скрипт с описанием структуры основной БД;
    - `utils.py` — скрипт со вспомогательными функциями;
    - `schemas.py` — скрипт с описанием схем запросов и ответов API;
  - `main.py` — основной скрипт приложения (точка входа);
  - `config.py` — скрипт с настройками приложения;
  - `database.py` — скрипт с инициализацией работы с БД;
  - `schemas.py` — скрипт с описанием схемы ответа корня API;
- `migrations/` — папка с описанием миграций БД с использованием Alembic;
- `alembic.ini` — конфигурационный файл Alembic;
- `Dockerfile` — конфигурационный файл Docker;
- `compose.yaml` — конфигурационный файл Docker Compose;
- `requirements.txt` — текстовый файл с перечислением зависимостей приложения;
- `.gitignore` — текстовый файл с перечислением исключённых из Git путей.

## Запуск проекта

Так как проект состоит из нескольких составных частей (FastAPI, PostgreSQL и Redis),
удобнее всего запускать его, используя **Docker Compose**.

При запущенном **Docker** для запуска сервиса достаточно выполнить команду:

```bash
docker compose up
```

## Методы API

### Root

#### GET `/`

Получение основной информации о приложении.

- Авторизация: **НЕТ**
- Кэширование: **ДА**

Пример ответа:

`200 OK`:

```json
{"info": "API для создания коротких ссылок", "status": "OK"}
```

### Auth

#### POST `/auth/register`

Регистрация пользователя.

- Авторизация: **НЕТ**
- Кэширование: **НЕТ**

Пример запроса:

```json
{
  "email": "user@example.com",
  "password": "password",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

Примеры ответов:

`201 Created`:

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

`400 Bad Request`:

```json
{"detail": "REGISTER_USER_ALREADY_EXISTS"}
```

#### POST `/auth/jwt/login`

Вход в аккаунт.

- Авторизация: **НЕТ**
- Кэширование: **НЕТ**

Пример запроса:

_x-www-form-urlencoded_
- username: user@example.com
- password: password

Примеры ответов:

`200 OK`:

```json
{"access_token": "TOKEN", "token_type": "bearer"}
```

`400 Bad Request`:

```json
{"detail": "LOGIN_BAD_CREDENTIALS"}
```

#### POST `/auth/jwt/logout`

Выход из аккаунта.

- Авторизация: **ДА**
- Кэширование: **НЕТ**

### Links

#### POST `/links/shorten`

Создание короткой ссылки.

- Авторизация: **ДА**
- Кэширование: **НЕТ**

Доступно только авторизованным пользователям,
чтобы сохранить создателя ссылки и в дальнейшем понимать, кому давать права на её изменение.

Пример запроса:

```json
{
  "url": "https://google.com",
  "custom_alias": "ggl",
  "expires_at": "2025-04-01"
}
```

Примеры ответов:

`201 Created`:

```json
{"info": "Link with short code ggl was created successfully"}
```

`422 Unprocessable Entity`:

```json
{"detail": "Custom alias must consist of 3 to 10 latin letters or numbers"}
```

`409 Conflict`:

```json
{"detail": "Custom alias is already taken"}
```

#### GET `/links/search?original_url={original_url}`

Поиск короткой ссылки по оригинальному URL.

- Авторизация: **НЕТ**
- Кэширование: **НЕТ**

Пример ответа:

`200 OK`:

```json
[
  {
    "short_code": "ggl",
    "original_url": "https://google.com/",
    "created_at": "2025-03-30T10:37:39.286933Z",
    "expires_at": null
  }
]
```

#### GET `/links/user`

Получение всех ссылок, созданных данным пользователем.

- Авторизация: **НЕТ**
- Кэширование: **НЕТ**

Пример ответа:

`200 OK`:

```json
[
  {
    "short_code": "ggl",
    "original_url": "https://google.com/",
    "created_at": "2025-03-30T10:37:39.286933Z",
    "expires_at": null
  }
]
```

#### GET `/links/{short_code}`

Использование короткой ссылки (перенаправление по оригинальному URL).

- Авторизация: **НЕТ**
- Кэширование: **НЕТ**

Я хотел сделать кэширование данного эндпоинта, но `RedirectResponse` перестаёт работать из-за кэширования.

Примеры ответов:

`308 Permanent Redirect`:

Успешное перенаправление на оригинальный URL.

`404 Not Found`:

```json
{"detail": "Link with short code ggl does not exist"}
```

#### GET `/links/{short_code}/stats`

Получение статистики использования короткой ссылки.

- Авторизация: **ДА**
- Кэширование: **ДА**

Примеры ответов:

`200 OK`:

```json
{
  "short_code":"ggl",
  "original_url":"https://google.com/",
  "created_at":"2025-03-30T10:37:39.286933Z",
  "expires_at":null,
  "redirect_count":1,
  "latest_redirect_at":"2025-03-30T12:14:38.074305Z"
}
```

`404 Not Found`:

```json
{"detail": "Link with short code ggl does not exist"}
```

`403 Forbidden`:

```json
{"detail": "You do not have the rights to view stats for the link with short code ggl"}
```

#### PUT `/links/{short_code}`

Обновление короткой ссылки.

- Авторизация: **ДА**
- Кэширование: **НЕТ**

Под обновлением подразумевается сохранение короткого кода и изменение оригинального URL или времени жизни.

Пример запроса:

```json
{
  "new_url": "https://yandex.ru",
  "expires_at": "2025-04-01"
}
```

Примеры ответов:

`200 OK`:

```json
{"info": "Link with short code ggl was updated successfully"}
```

`404 Not Found`:

```json
{"detail": "Link with short code ggl does not exist"}
```

`422 Unprocessable Entity`:

```json
{"detail": "Field expires_at must be a datetime, False or None"}
```

#### DELETE `/links/{short_code}`

Удаление короткой ссылки.

- Авторизация: **ДА**
- Кэширование: **НЕТ**

Примеры ответов:

`200 OK`:

```json
{"info": "Link with short code ggl was deleted successfully"}
```

`404 Not Found`:

```json
{"detail": "Link with short code ggl does not exist"}
```

`403 Forbidden`:

```json
{"detail": "You do not have the rights to delete the link with short code ggl"}
```
