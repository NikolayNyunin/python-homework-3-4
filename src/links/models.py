from sqlalchemy import Column, String, TIMESTAMP, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from datetime import datetime, timezone

Base = declarative_base()


class Link(Base):
    __tablename__ = 'links'

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    short_code = Column(String, nullable=False)
    original_url = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), nullable=False)
    expires_at = Column(TIMESTAMP, nullable=True)
