# tests/domain/logics/test_validate_trade_date.py
import pytest
from datetime import date, datetime, timedelta

from src.domain.logics.validate_trade_date import validate_and_convert_trade_date


def test_validate_and_convert_trade_date_valid_string():
    valid_date_str = "2021-01-01"
    expected_date = date(2021, 1, 1)
    assert validate_and_convert_trade_date(valid_date_str) == expected_date

def test_validate_and_convert_trade_date_valid_date():
    valid_date = date(2021, 1, 1)
    assert validate_and_convert_trade_date(valid_date) == valid_date

def test_validate_and_convert_trade_date_invalid_string_format():
    invalid_date_str = "2021-31-01"
    with pytest.raises(ValueError) as excinfo:
        validate_and_convert_trade_date(invalid_date_str)
    assert "trade_dateが無効な日付フォーマットです。" in str(excinfo.value)

def test_validate_and_convert_trade_date_future_date():
    future_date = (datetime.now() + timedelta(days=1)).date()
    with pytest.raises(ValueError) as excinfo:
        validate_and_convert_trade_date(future_date)
    assert "取引日は過去または今日でなければなりません。" in str(excinfo.value)

def test_validate_and_convert_trade_date_invalid_type():
    invalid_type = 12345
    with pytest.raises(TypeError) as excinfo:
        validate_and_convert_trade_date(invalid_type)
    assert "trade_datesの項目はstrまたはdate型である必要があります。" in str(excinfo.value)

def test_validate_and_convert_trade_date_none():
    assert validate_and_convert_trade_date(None) is None
