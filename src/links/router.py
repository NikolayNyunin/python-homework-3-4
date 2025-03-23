from fastapi import APIRouter

router = APIRouter(prefix='/links', tags=['links'])


@router.post('/shorten')
async def create():
    """Создание короткой ссылки."""

    pass


@router.get('/{short_code}')
async def redirect(short_link: str):
    """Использование короткой ссылки (перенаправление на оригинальную страницу)."""

    pass


@router.put('/{short_code}')
async def update(short_code: str):
    """Обновление короткой ссылки."""

    pass


@router.delete('/{short_code}')
async def delete(short_code: str):
    """Удаление короткой ссылки."""

    pass


@router.get('/{short_code}/stats')
async def get_stats(short_link: str):
    """Получение статистики использования короткой ссылки."""

    pass


@router.get('/search')
async def search(original_url: str):
    """Поиск короткой ссылки по оригинальному URL."""

    pass
