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
])
def test_convert_price_format(input_value: str, expected_output: float | None):
    assert convert_price_format(input_value) == expected_output

@pytest.mark.parametrize("input_value", [
    "5'",        # 分数部分がないためエラーを期待
    "-5'",       # 分数部分がないためエラーを期待
    "abc",       # 異常値
    # その他無効なフォーマットのテストケースをここに追加
])
def test_convert_price_format_invalid_input(input_value: str):
    with pytest.raises(ValueError) as excinfo:
        convert_price_format(input_value)
    assert "Invalid price format" in str(excinfo.value)
