import pytest
from src.domain.value_objects.name import Name

def test_name_success():
    """正しい名前の長さでNameオブジェクトを作成できることを検証"""
    name_str = "Valid Name"
    name_obj = Name(name=name_str)
    assert name_obj.to_primitive() == name_str

def test_name_empty():
    """空の名前でNameオブジェクトを作成しようとした時にValueErrorが発生することを検証"""
    with pytest.raises(ValueError) as excinfo:
        Name(name="")
    assert "名前は空にできません。" in str(excinfo.value)

def test_name_too_long():
    """名前が64文字を超える場合にValueErrorが発生することを検証"""
    long_name = "a" * 65  # 65文字の名前
    with pytest.raises(ValueError) as excinfo:
        Name(name=long_name)
    assert "名前は64文字以内である必要があります。" in str(excinfo.value)
