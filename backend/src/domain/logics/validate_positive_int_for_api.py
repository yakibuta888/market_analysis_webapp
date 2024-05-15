# src/domain/logics/validate_positive_int_for_api.py
from src.settings import logger


def validate_positive_int(value: int, field: str) -> int:
    logger.debug(f"{field}の値を検証します。value={value}")
    if value < 0:
        raise ValueError(f"{field}の値は0以上でなければなりません。")
    return value
