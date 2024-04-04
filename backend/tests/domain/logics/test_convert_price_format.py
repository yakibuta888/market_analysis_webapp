# test/domain/logics/test_convert_price_format.py
import pytest
from src.domain.logics.convert_price_format import convert_price_format

@pytest.mark.parametrize("input_value,expected_output", [
    ("-'27", -0.84375),
    ("+'27", 0.84375),
    ("-'010", -0.0003125),
    ("+'010", 0.0003125),
    ("-5'010", -5.0003125),
    ("+5'010", 5.0003125),
    ("5'010", 5.0003125),
    ("-.27", -0.27),
    ("+.27", 0.27),
    ("-27", -27),
    ("+27", 27),
    ("0", 0.0),
    ("5", 5.0),
    ("-5", -5.0),
    ("5.25", 5.25),
    ("-5.25", -5.25),
    ("0'27", 0.84375),
    ("0'010", 0.0003125),
    ("-", None),
    ("", None),
    (None, None),
    # カンマ入り数値
    ("1,234", 1234.0),
    ("12,345", 12345.0),
    ("123,456", 123456.0),
    ("1,234,567", 1234567.0),
    ("-1,234", -1234.0),
    # AやBが付いた数値
    ("100A", 100.0),
    ("-100B", -100.0),
    # 分数表記
    ("1'16", 1 + 16/32),
    ("-1'16", -(1 + 16/32)),
    # カンマとA/Bが組み合わさったケース
    ("1,234A", 1234.0),
    ("-1,234B", -1234.0),
    ("2,468'16A", 2468 + 16/32),
    ("-2,468'16B", -(2468 + 16/32)),
    # カンマ入りで分数が付くケース
    ("1,000'16", 1000 + 16/32),
    ("-1,000'16", -(1000 + 16/32)),
])
def test_convert_price_format(input_value: str | None, expected_output: float | None):
    assert convert_price_format(input_value) == expected_output

@pytest.mark.parametrize("input_value", [
    "5'",        # 分数部分がないためエラーを期待
    "-5'",       # 分数部分がないためエラーを期待
    "abc",       # 異常値
    # その他無効なフォーマットのテストケースをここに追加
    "1,234'",
    "1,234.56.78",
    "ABC",
])
def test_convert_price_format_invalid_input(input_value: str):
    with pytest.raises(ValueError) as excinfo:
        convert_price_format(input_value)
    assert "Invalid price format" in str(excinfo.value)
