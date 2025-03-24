from pydantic import BaseModel

from datetime import datetime


class CreateRequest(BaseModel):
    url: str
    custom_alias: str = None
    expires_at: datetime = None


class UpdateRequest(BaseModel):
    new_url: str


class APIResponse(BaseModel):
    info: str


class StatsResponse(BaseModel):
    pass


class SearchResponse(BaseModel):
    short_code: str
    short_url: str
