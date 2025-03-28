from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from datetime import datetime, timezone

Base = declarative_base()


class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID, nullable=False)
    short_code = Column(String, unique=True, nullable=False)
    original_url = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=True)
