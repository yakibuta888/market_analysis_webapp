import pytest
from src.domain.value_objects.password import Password


def test_password_hashing_and_verification():
    plain_password = "StrongPassword123"
    password_vo = Password.create(plain_password)

    # Verify that the hashed password is not the same as the plain password
    assert password_vo.hashed_password != plain_password

    # Verify that the hashed password can be verified
    assert Password.verify_password(plain_password, password_vo.hashed_password)

    # Verify that an incorrect password does not match
    assert not Password.verify_password("wrongpassword", password_vo.hashed_password)


def test_create_invalid_password():
    with pytest.raises(ValueError) as exc_info:
        Password.create("weak")
    assert "パスワードは8文字以上である必要があります。" in str(exc_info.value)

    with pytest.raises(ValueError):
        Password.create("")


def test_verify_password():
    plain_password = "AnotherStrongPassword123"
    hashed_password = Password._hash_password(plain_password)
    assert Password.verify_password(plain_password, hashed_password)
    assert not Password.verify_password("wrongpassword", hashed_password)


def test_password_from_db():
    hashed_password = Password._hash_password("securepassword")
    password_vo = Password.from_db(hashed_password)

    # Verify that the hashed password matches
    assert password_vo.hashed_password == hashed_password

    # Verify that the hashed password can be verified
    assert Password.verify_password("securepassword", password_vo.hashed_password)

def test_password_direct_initialization():
    with pytest.raises(NotImplementedError, match="Password value object must be created through 'create' or 'from_db' methods"):
        Password("hashed_password")
