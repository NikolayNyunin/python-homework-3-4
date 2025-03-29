from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID, nullable=False)
    short_code = Column(String, unique=True, nullable=False)
    original_url = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=True)

    logs = relationship('Redirect', back_populates='link', cascade='all, delete-orphan')


class Redirect(Base):
    __tablename__ = 'redirects'

    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey('links.id', ondelete='CASCADE'), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    link = relationship('Link', back_populates='logs')
