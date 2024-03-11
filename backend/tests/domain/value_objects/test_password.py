import pytest
from src.domain.value_objects.password import Password

def test_create_valid_password():
    plain_password = "StrongPassword123"
    password = Password.create(plain_password)
    assert password is not None
    assert Password.verify_password(plain_password, password.hashed_password)

def test_create_invalid_password():
    with pytest.raises(ValueError) as exc_info:
        Password.create("weak")
    assert "パスワードは8文字以上である必要があります。" in str(exc_info.value)

def test_verify_password():
    plain_password = "AnotherStrongPassword123"
    hashed_password = Password.hash_password(plain_password)
    assert Password.verify_password(plain_password, hashed_password)
    assert not Password.verify_password("wrongpassword", hashed_password)
