import pytest
from datetime import date
from src.domain.value_objects.trade_date import TradeDate

def test_trade_date_from_string_success():
    # 正しい日付形式の文字列を与えた場合のテスト
    date_str = "Friday, 08 Mar 2024"
    expected_date = date(2024, 3, 8)
    trade_date = TradeDate.from_string(date_str)
    assert trade_date.to_date() == expected_date, "TradeDate.from_string should parse the date correctly."

def test_trade_date_from_string_invalid_format():
    # 不正な日付形式の文字列を与えた場合のテスト
    invalid_date_str = "Invalid Date Format"
    with pytest.raises(ValueError) as excinfo:
        TradeDate.from_string(invalid_date_str)
    assert "Invalid date format" in str(excinfo.value), "TradeDate.from_string should raise ValueError for invalid formats."

def test_trade_date_direct_initialization():
    # date 型の値から直接 TradeDate を作成するテスト
    input_date = date(2024, 3, 8)
    trade_date = TradeDate(input_date)
    assert trade_date.to_date() == input_date, "Direct initialization of TradeDate with a date object should work correctly."

def test_trade_date_initialization_with_non_date_type():
    # 非 date 型の値で TradeDate を作成しようとした場合のテスト
    with pytest.raises(ValueError) as excinfo:
        TradeDate("2024-03-08") # type: ignore
    assert "TradeDate must be a date instance." in str(excinfo.value), "TradeDate initialization should raise ValueError for non-date types."

def test_trade_date_to_string_with_default_format():
    # デフォルトフォーマットでのテスト
    trade_date = TradeDate(date(2024, 4, 2))
    expected_date_str = "2024-04-02"
    assert trade_date.to_string() == expected_date_str, "TradeDate should convert to string in YYYY-MM-DD format"

def test_trade_date_to_string_with_custom_format():
    # カスタムフォーマットでのテスト
    trade_date = TradeDate(date(2024, 3, 8))
    expected_date_str = "08-Mar-2024"
    # カスタムフォーマット指定
    assert trade_date.to_string("%d-%b-%Y") == expected_date_str, "TradeDate should convert to string in DD-MMM-YYYY format"
