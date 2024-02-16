# src/api/dependencies.py

import os

from sqlalchemy.orm import Session
from typing import Generator
from typing import Any

from src.settings import logger
from src.domain.services.user_service import UserService
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.repositories.user_repository_mysql import UserRepositoryMysql
from src.infrastructure.mock.mock_user_repository import MockUserRepository
from src.infrastructure.database.database import db_session


def get_user_repository() -> UserRepository:
    logger.info("Fetching UserRepositoryMysql")
    session = get_db()  # Create a session
    return UserRepositoryMysql(session)  # Pass the session parameter

def get_user_service():
    user_repository = get_user_repository()
    return UserService(user_repository)

def get_db() -> Generator[Session, Any, Any]:
    db = db_session()
    try:
        yield db
    finally:
        db.close()
