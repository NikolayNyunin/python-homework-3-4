from pydantic import BaseModel

from datetime import datetime


class CreateRequest(BaseModel):
    url: str
    custom_alias: str | None = None
    expires_at: datetime | None = None


class UpdateRequest(BaseModel):
    new_url: str
    expires_at: datetime | None = None


class APIResponse(BaseModel):
    info: str


class StatsResponse(BaseModel):
    pass


class SearchResponse(BaseModel):
    short_code: str
    original_url: str
    created_at: datetime
    expires_at: datetime | None = None
