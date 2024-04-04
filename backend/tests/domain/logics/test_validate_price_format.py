# tests/domain/logics/test_validate_price_format.py
import pytest

from src.domain.logics.validate_price_format import validate_price_format


@pytest.mark.parametrize("input_value,expected", [
    ("-'27", True),
    ("+'27", True),
    ("-'010", True),
    ("+'010", True),
    ("-5'010", True),
    ("+5'010", True),
    ("5'010", True),
    ("-.27", True),
    ("+.27", True),
    ("-27", True),
    ("+27", True),
    ("0", True),
    ("5", True),
    ("-5", True),
    ("5.25", True),
    ("-5.25", True),
    ("0'27", True),
    ("0'010", True),
    ("5'", False),  # 分数部分がないためエラーを期待
    ("-5'", False),  # 分数部分がないためエラーを期待
    ("abc", False),  # 異常値
    # 末尾にAまたはBが付くケース
    ("123A", True),
    ("-123B", True),
    ("5'27A", True),
    ("-5'27B", True),
    ("123.45A", True),
    ("-123.45B", True),
    ("0A", True),
    ("0B", True),
    ("-'010A", True),
    ("+'010B", True),
    # 末尾にAまたはBが付いているが不正な形式
    ("5'A", False),
    ("-5'B", False),
    ("abcA", False),
    ("abcB", False),
    # 適切にカンマが使用されているケース
    ("1,000", True),
    ("10,000", True),
    ("100,000", True),
    ("1,000,000", True),
    ("-1,234,567", True),
    ("+1,234,567", True),
    ("1,234,567.89", True),
    ("1,000,000A", True),
    ("2,000,000B", True),
    # カンマ直後に3桁以外の数字が来るケース（不適切な使用）
    ("1,2345", False),
    ("12,34", False),
    ("123,4", False),
    # カンマ直前が3桁以外で始まるケース
    ("1,234", True),
    ("12,345", True),
    ("123,456", True),
    # 分数と組み合わせたケース
    ("1,234'567", True),
    ("-1,234'567", True),
    ("+1,234'567", True),
    # 不正なフォーマット
    ("1,23,456", False),
    ("123,", False),
    (",123", False),
    ("1,2,3", False),
    ("1,234'", False),
])
def test_validate_price_format(input_value: str, expected: bool):
    if expected:
        assert validate_price_format(input_value)
    else:
        with pytest.raises(ValueError):
            validate_price_format(input_value)
