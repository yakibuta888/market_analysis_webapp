# src/infrastructure/database/database.py
# coding: utf-8
import os
import re
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from src.settings import logger


encoded_password = quote_plus(os.getenv('MYSQL_PASSWORD', ''))
DATABASE_URL_BASE: str = f"{os.getenv('DIALECT')}+{os.getenv('DRIVER')}://{os.getenv('MYSQL_USER')}:{encoded_password}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}"

DATABASE_URL = f"{DATABASE_URL_BASE}/{os.getenv('MYSQL_DATABASE')}"
TEST_DATABASE_URL: str = f"{DATABASE_URL_BASE}/test_database"


def check_database_url(database_url: str) -> None:
    """
    Check if the database URL is valid
    """
    pattern = r"^\w+\+\w+://\w+:.*@[\w\.]+(:\d+)?/[\w-]+$"
    database_url_notice = database_url.replace(encoded_password, f"{'*' * 5}")

    if not re.match(pattern, database_url):
        logger.error(f"Invalid database URL: {database_url_notice}")
        raise ValueError(f"Invalid database URL: {database_url_notice}")

    logger.info(f"Database URL is valid: {database_url_notice}")

def get_database_url(testing: bool = False) -> str:
    """
    Get the database URL
    """
    database_url = TEST_DATABASE_URL if testing else DATABASE_URL
    check_database_url(database_url)
    return database_url

def get_engine(testing: bool = False):
    """
    Get the database engine
    """
    database_url = get_database_url(testing)
    return create_engine(
        database_url,
        echo=True
    )


engine = get_engine()
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
Base = declarative_base()
Base.query = db_session.query_property()
