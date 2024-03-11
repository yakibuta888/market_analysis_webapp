import pytest
from datetime import date
from src.domain.value_objects.year_month import YearMonth

@pytest.mark.parametrize("input_string, expected_year, expected_month", [
    ("APR 24", 2024, 4),
    ("DEC 23", 2023, 12),
])
def test_year_month_from_string(input_string: str, expected_year: int, expected_month: int):
    year_month = YearMonth.from_string(input_string)
    assert year_month.year == expected_year
    assert year_month.month == expected_month

@pytest.mark.parametrize("year, month, expected_string", [
    (2024, 4, "2024-04"),
    (2023, 12, "2023-12"),
])
def test_year_month_to_db_format(year: int, month: int, expected_string: str):
    year_month = YearMonth(year, month)
    assert year_month.to_db_format() == expected_string

# NOTE: 以下のテストは、YearMonth.from_date() メソッドが実装された場合に有効です。
# @pytest.mark.parametrize("input_date, expected_year, expected_month", [
#     (date(2024, 4, 1), 2024, 4),
#     (date(2023, 12, 1), 2023, 12),
# ])
# def test_year_month_from_date(input_date, expected_year, expected_month):
#     year_month = YearMonth.from_date(input_date)
#     assert year_month.year == expected_year
#     assert year_month.month == expected_month

@pytest.mark.parametrize("input_string, expected_year, expected_month", [
    ("2024-04", 2024, 4),
    ("2023-12", 2023, 12),
])
def test_year_month_from_db_format(input_string: str, expected_year: int, expected_month: int):
    year_month = YearMonth.from_db_format(input_string)
    assert year_month.year == expected_year
    assert year_month.month == expected_month
