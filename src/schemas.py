from pydantic import BaseModel


class RootResponse(BaseModel):
    info: str
    status: str
