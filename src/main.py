from src.links.router import router as links_router
from src.schemas import RootResponse
from src.auth.users import auth_backend, current_active_user, fastapi_users
from src.auth.schemas import UserCreate, UserRead

from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(title='Link shortening API', lifespan=lifespan)

app.include_router(links_router)
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=['auth'])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix='/auth', tags=['auth'])


@app.get('/', response_model=RootResponse)
async def root():
    """Получение основной информации о приложении."""

    return {'info': 'API для создания коротких ссылок', 'status': 'OK'}


if __name__ == '__main__':
    uvicorn.run('src.main:app', host='0.0.0.0', reload=True)
