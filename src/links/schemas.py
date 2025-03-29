from pydantic import BaseModel, HttpUrl

from datetime import datetime


class CreateRequest(BaseModel):
    url: HttpUrl
    custom_alias: str | None = None
    expires_at: datetime | None = None


class UpdateRequest(BaseModel):
    new_url: HttpUrl
    expires_at: datetime | bool | None = None


class APIResponse(BaseModel):
    info: str


class StatsResponse(BaseModel):
    short_code: str
    original_url: HttpUrl
    created_at: datetime
    expires_at: datetime | None
    redirect_count: int
    latest_redirect_at: datetime | None


class SearchResponse(BaseModel):
    short_code: str
    original_url: HttpUrl
    created_at: datetime
    expires_at: datetime | None
