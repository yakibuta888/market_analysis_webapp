# coding: utf-8
import os
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from src.settings import logger


DATABASE_URL_BASE: str = f"{os.getenv('DIALECT')}+{os.getenv('DRIVER')}://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}"

if os.getenv('TEST_DATABASE') == 'True':
    database_url: str = f"{DATABASE_URL_BASE}/test_database"
else:
    database_url = f"{DATABASE_URL_BASE}/{os.getenv('MYSQL_DATABASE')}"

pattern = r"^\w+\+\w+://\w+:\w+@\w+(:\d+)?/\w+$"
database_url_notice = database_url.replace(os.getenv('MYSQL_PASSWORD', ''), f"{'*' * len(os.getenv('MYSQL_PASSWORD', ''))}")

if not re.match(pattern, database_url):
    logger.error(f"Invalid database URL: {database_url_notice}")
    raise ValueError(f"Invalid database URL: {database_url_notice}")

logger.info(f"Database URL is valid: {database_url_notice}")

engine = create_engine(
    database_url,
    connect_args={"check_same_thread": False},
    echo=True
)
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
Base = declarative_base()
Base.query = db_session.query_property()
