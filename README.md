# Домашние задания №3,4 (Applied Python)

![Python](https://img.shields.io/badge/python-v3.12-blue.svg)

## Оглавление

- [Описание](#описание)
- [Структура проекта](#структура-проекта)
- [Структура БД](#структура-бд)
  - [Таблица links](#таблица-links)
  - [Таблица redirects](#таблица-redirects)
- [Запуск проекта](#запуск-проекта)
- [Методы API](#методы-api)
  - [Root](#1-root)
    - [GET /](#11-get-)
  - [Auth](#2-auth)
    - [POST /auth/register](#21-post-authregister)
    - [POST /auth/jwt/login](#22-post-authjwtlogin)
    - [POST /auth/jwt/logout](#23-post-authjwtlogout)
  - [Links](#3-links)
    - [POST /links/shorten](#31-post-linksshorten)
    - [GET /links/search?original_url={original_url}](#32-get-linkssearchoriginal_urloriginal_url)
    - [GET /links/user](#33-get-linksuser)
    - [GET /links/{short_code}](#34-get-linksshort_code)
    - [GET /links/{short_code}/stats](#35-get-linksshort_codestats)
    - [PUT /links/{short_code}](#36-put-linksshort_code)
    - [DELETE /links/{short_code}](#37-delete-linksshort_code)
- [Тестирование](#тестирование)
  - [Покрытие кода](#покрытие-кода)
  - [Запуск тестов](#запуск-тестов)
  - [Юнит-тестирование](#юнит-тестирование)
  - [Функциональное тестирование](#функциональное-тестирование)
  - [Нагрузочное тестирование](#нагрузочное-тестирование)

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
- Тестирование приложения с использованием **pytest** и **Locust**.

Ссылка на развёрнутый сервис: [https://python-homework-3-4.onrender.com](https://python-homework-3-4.onrender.com)
(используется бесплатный тариф хостинга, так что сервер может отвечать медленно или не отвечать совсем).

## Структура проекта

- `task1.ipynb` — Jupyter-ноутбук с описанием требований к ДЗ 3;
- `task2.ipynb` — Jupyter-ноутбук с описанием требований к ДЗ 4;
- `README.md` — Markdown-файл с документацией приложения ***(данный файл)***;
- `docker/` — папка со скриптом для запуска Docker;
  - `start.sh` — скрипт для запуска сервера;
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
- `tests/` — папка с тестами;
  - `unit/` — папка с юнит-тестами;
    - `test_utils.py` — скрипт с юнит-тестами для функций из src.links.utils;
  - `functional/` — папка с функциональными тестами для эндпоинтов API;
    - `test_root.py` — скрипт с тестами для функции src.main.root;
    - `test_create.py` — скрипт с тестами для функции src.links.router.create;
    - `test_search.py` — скрипт с тестами для функции src.links.router.search;
    - `test_get_user_links.py` — скрипт с тестами для функции src.links.router.get_user_links;
    - `test_redirect.py` — скрипт с тестами для функции src.links.router.redirect;
    - `test_get_stats.py` — скрипт с тестами для функции src.links.router.get_stats;
    - `test_update.py` — скрипт с тестами для функции src.links.router.update;
    - `test_delete.py` — скрипт с тестами для функции src.links.router.delete;
  - `load/` — папка с нагрузочными тестами;
    - `locustfile.py` — скрипт с конфигурацией нагрузочного тестирования Locust;
  - `conftest.py` — скрипт с конфигурацией pytest;
- `migrations/` — папка с описанием миграций БД с использованием Alembic;
- `alembic.ini` — конфигурационный файл Alembic;
- `Dockerfile` — конфигурационный файл Docker;
- `compose.yaml` — конфигурационный файл Docker Compose;
- `requirements.txt` — текстовый файл с перечислением зависимостей приложения;
- `.gitignore` — текстовый файл с перечислением исключённых из Git путей.

## Структура БД

Основная база данных приложения для хранения информации о коротких ссылках имеет следующую структуру:

### Таблица `links`

Описывает сами короткие ссылки.

|     Поле     |        Тип данных        | Обязательное | Уникальное |   По умолчанию    |                  Описание                   |
|:------------:|:------------------------:|:------------:|:----------:|:-----------------:|:-------------------------------------------:|
|      id      |         Integer          |   Да (PK)    |     Да     |         -         |               Первичный ключ                |
|   user_id    |           UUID           |      Да      |    Нет     |         -         | Идентификатор пользователя-создателя ссылки |
|  short_code  |          String          |      Да      |     Да     |         -         |             Короткий код ссылки             |
| original_url |          String          |      Да      |    Нет     |         -         |              Оригинальный URL               |
|  created_at  | TIMESTAMP(timezone=True) |      Да      |    Нет     | CURRENT_TIMESTAMP |        Дата и время создания ссылки         |
|  expires_at  | TIMESTAMP(timezone=True) |     Нет      |    Нет     |         -         |  Дата и время истечения срока жизни ссылки  |

**Связи:**
- Имеет отношение "один-ко-многим" с таблицей `redirects` через поле `logs`

### Таблица `redirects`

Описывает факты переходов по коротким ссылкам.

|    Поле    |        Тип данных        | Обязательное | Уникальное |   По умолчанию    |       Описание        |
|:----------:|:------------------------:|:------------:|:----------:|:-----------------:|:---------------------:|
|     id     |         Integer          |   Да (PK)    |     Да     |         -         |    Первичный ключ     |
|  link_id   |         Integer          |   Да (FK)    |    Нет     |         -         | Идентификатор ссылки  |
| timestamp  | TIMESTAMP(timezone=True) |      Да      |    Нет     | CURRENT_TIMESTAMP | Время перенаправления |

**Связи:**
- Имеет отношение "многие-к-одному" с таблицей `links` через поле `link`
- Внешний ключ `link_id` ссылается на `links.id` с каскадным удалением (ON DELETE CASCADE)

## Запуск проекта

Так как проект состоит из нескольких составных частей (FastAPI, PostgreSQL и Redis),
удобнее всего запускать его, используя **Docker Compose**.

При запущенном **Docker** для запуска сервиса достаточно выполнить команду:

```bash
docker compose up
```

## Методы API

### 1. Root

#### 1.1. GET `/`

Получение основной информации о приложении.

- Авторизация: **НЕТ**
- Кэширование: **ДА**

Пример ответа:

`200 OK`:

```json
{"info": "API для создания коротких ссылок", "status": "OK"}
```

### 2. Auth

#### 2.1. POST `/auth/register`

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

#### 2.2. POST `/auth/jwt/login`

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

#### 2.3. POST `/auth/jwt/logout`

Выход из аккаунта.

- Авторизация: **ДА**
- Кэширование: **НЕТ**

### 3. Links

#### 3.1. POST `/links/shorten`

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

#### 3.2. GET `/links/search?original_url={original_url}`

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

#### 3.3. GET `/links/user`

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

#### 3.4. GET `/links/{short_code}`

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

#### 3.5. GET `/links/{short_code}/stats`

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

#### 3.6. PUT `/links/{short_code}`

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

#### 3.7. DELETE `/links/{short_code}`

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

## Тестирование

Для проверки работоспособности приложения были реализованы юнит- и функциональные тесты с использованием **pytest**,
а также было проведено нагрузочное тестирование при помощи **Locust**.

### Покрытие кода

[//]: # (TODO: work in progress)

### Запуск тестов

При условии установленных зависимостей из `requirements.txt`,
запустить юнит- и функциональные тесты и проверить процент покрытия кода можно при помощи команды:

```bash
python -m pytest --cov=src --cov-report=term-missing
```

Для проведения нагрузочного тестирования можно использовать команду:

```bash
locust -f tests/load/locustfile.py
```

После выполнения этой команды необходимо перейти в [веб-интерфейс Locust](http://localhost:8089),
чтобы настроить интенсивность нагрузки и указать URL сервиса
([http://localhost:9999/](http://localhost:9999/) при локальном запуске приложения).

### Юнит-тестирование

Юнит-тестами я покрыл только вспомогательные функции из файла `src/links/utils.py`,
отвечающие за проверку и генерацию кодов коротких ссылок.
Остальной код приложения удобнее и логичнее проверять функциональными тестами.

### Функциональное тестирование

[//]: # (TODO: work in progress)

### Нагрузочное тестирование

[//]: # (TODO: work in progress)
