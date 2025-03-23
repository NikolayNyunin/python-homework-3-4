from src.links.router import router as links_router

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(title='Link shortening API', lifespan=lifespan)

app.include_router(links_router)


class RootResponse(BaseModel):
    info: str
    status: str


@app.get('/', response_model=RootResponse)
async def root():
    """Получение основной информации о приложении."""

    return {'info': 'API для создания коротких ссылок', 'status': 'OK'}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', reload=True)
