# src/infrastructure/database/database.py
# coding: utf-8
import os
import re
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from src.settings import logger


def get_engine():
    """
    Get the database engine
    """
    encoded_password = quote_plus(os.getenv('MYSQL_PASSWORD', ''))
    database_url: str = f"{os.getenv('DIALECT')}+{os.getenv('DRIVER')}://{os.getenv('MYSQL_USER')}:{encoded_password}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"

    # Check if the database URL is valid
    pattern = r"^\w+\+\w+://\w+:.*@[\w\.]+(:\d+)?/[\w-]+$"
    database_url_notice = database_url.replace(encoded_password, f"{'*' * 5}")

    if not re.match(pattern, database_url):
        logger.error(f"Invalid database URL: {database_url_notice}")
        raise ValueError(f"Invalid database URL: {database_url_notice}")

    logger.info(f"Database URL is valid: {database_url_notice}")
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
