# tests/domain/logics/test_date_time_utilities.py
import pytest
from datetime import datetime
import pytz
from src.domain.logics.date_time_utilities import parse_datetime

def test_parse_datetime_correct_format():
    input_date = "03 May 2024 10:32:00 PM CT"
    expected_date = datetime(2024, 5, 4, 3, 32, 0, tzinfo=pytz.utc)
    assert parse_datetime(input_date) == expected_date, "The UTC conversion did not match the expected output"

def test_parse_datetime_incorrect_format():
    input_date = "03-05-2024 10:32:00 PM"
    with pytest.raises(ValueError) as excinfo:
        parse_datetime(input_date)
    assert "日付フォーマットが正しくありません" in str(excinfo.value), "Expected ValueError for incorrect date format"

def test_parse_datetime_timezone_conversion():
    input_date = "03 May 2024 10:32:00 PM CT"
    result = parse_datetime(input_date)
    expected_timezone = pytz.utc
    assert result.tzinfo == expected_timezone, "The timezone of the parsed datetime should be UTC"
