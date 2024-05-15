# tests/domain/logics/test_validate_positive_int_for_api.py
import pytest
from src.domain.logics.validate_positive_int_for_api import validate_positive_int

def test_validate_positive_int_valid():
    assert validate_positive_int(0, 'skip') == 0
    assert validate_positive_int(10, 'limit') == 10

def test_validate_positive_int_invalid():
    with pytest.raises(ValueError) as excinfo:
        validate_positive_int(-1, 'skip')
    assert "skipの値は0以上でなければなりません。" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        validate_positive_int(-10, 'limit')
    assert "limitの値は0以上でなければなりません。" in str(excinfo.value)
