import pytest
from datetime import datetime
from src.domain.value_objects.year_month import YearMonth

@pytest.mark.parametrize("input_string, expected_year, expected_month", [
    ("APR 24", 2024, 4),
    ("APR 2024", 2024, 4),
    ("JUL 23", 2023, 7),
    ("DEC 2022", 2022, 12),
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


# 不正な省略形とその修正をテストするテストケース
@pytest.mark.parametrize("input_str, expected_result", [
    ("JLY 24", datetime(year=2024, month=7, day=1)),
    ("JUL 24", datetime(year=2024, month=7, day=1)),
    ("FEB 22", datetime(year=2022, month=2, day=1)),
    # 他の月のテストケースも追加可能
])
def test_from_string_with_various_inputs(input_str: str, expected_result: datetime):
    result = YearMonth.from_string(input_str)
    assert result.year == expected_result.year and result.month == expected_result.month, f"Test failed for input: {input_str}"

# 不正なフォーマットに対する例外が投げられるかテスト
@pytest.mark.parametrize("invalid_input", [
    "ABC 24",
    "123",
    "",
    "JLY24",  # 空白なし
])
def test_from_string_with_invalid_input(invalid_input: str):
    with pytest.raises(ValueError) as exc_info:
        YearMonth.from_string(invalid_input)
    assert "Invalid month format" in str(exc_info.value), f"Test failed for input: {invalid_input}"
