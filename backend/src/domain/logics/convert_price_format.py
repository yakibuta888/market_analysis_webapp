# src/domain/logics/convert_price_format.py
from src.settings import logger


def convert_price_format(value: str) -> float | None:
    if value == "-":
        return None
    value = value.strip("AB")  # AまたはBが末尾にある場合に除去
    try:
        if "'" in value:
            whole, fraction = value.split("'")
            if fraction.startswith("0"):
                float_fraction = float(f"0.{fraction}") / 32
            else:
                float_fraction = float(fraction) / 32
            if whole == "-":
                return -1 * float_fraction
            elif whole == "+":
                return float_fraction
            elif whole.startswith("-"):
                return float(whole) - float_fraction
            else:
                return float(whole) + float_fraction
        return float(value)
    except ValueError as e:
        logger.error(f"Failed to convert price format: {value}\n{e}")
        raise ValueError(f"Invalid price format: {value}") from e
