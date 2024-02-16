import os
import re

from src.settings import logger


DATABASE_URL_BASE: str = f"{os.getenv('DIALECT')}+{os.getenv('DRIVER')}://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}"

DATABASE_URL = f"{DATABASE_URL_BASE}/{os.getenv('MYSQL_DATABASE')}"
TEST_DATABASE_URL: str = f"{DATABASE_URL_BASE}/test_database"


def check_database_url(database_url: str) -> None:
    """
    Check if the database URL is valid
    """
    pattern = r"^\w+\+\w+://\w+:.*@[\w\.]+(:\d+)?/[\w-]+$"
    password = os.getenv('MYSQL_PASSWORD', '')
    database_url_notice = database_url.replace(password, f"{'*' * len(password)}")

    if not re.match(pattern, database_url):
        logger.error(f"Invalid database URL: {database_url_notice}")
        raise ValueError(f"Invalid database URL: {database_url_notice}")

    logger.info(f"Database URL is valid: {database_url_notice}")


check_database_url(DATABASE_URL)
check_database_url(TEST_DATABASE_URL)
