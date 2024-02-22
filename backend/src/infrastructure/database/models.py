# src/infrastructure/database/models.py

from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    name = Column(String(64), nullable=False)
