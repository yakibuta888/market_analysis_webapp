# tests/infrastructure/authentication/test_verification_token.py
import os
import pytest
import time
from itsdangerous import URLSafeTimedSerializer

from src.domain.exceptions.credentials_error import CredentialsError


@pytest.fixture(scope='function', autouse=True)
def set_test_env_vars():
    original_secret_key = os.getenv('SECRET_KEY')
    original_salt = os.getenv('SECURITY_PASSWORD_SALT')

    os.environ['SECRET_KEY'] = 'test_secret_key'
    os.environ['SECURITY_PASSWORD_SALT'] = 'test_salt'

    yield

    if original_secret_key is not None:
        os.environ['SECRET_KEY'] = original_secret_key
    else:
        del os.environ['SECRET_KEY']

    if original_salt is not None:
        os.environ['SECURITY_PASSWORD_SALT'] = original_salt
    else:
        del os.environ['SECURITY_PASSWORD_SALT']


def test_generate_verification_token():
    from src.infrastructure.authentication.verification_token import generate_verification_token
    test_email = "test@example.com"
    token = generate_verification_token(test_email)
    assert token is not None

def test_confirm_verification_token_success():
    from src.infrastructure.authentication.verification_token import confirm_verification_token
    test_email = "test@example.com"

    # テスト用の秘密鍵とソルトでトークンを生成
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY', 'test_secret_key'))
    token = serializer.dumps(test_email, salt=os.getenv('SECURITY_PASSWORD_SALT'))

    print(os.getenv('SECRET_KEY', ''), os.getenv('SECURITY_PASSWORD_SALT', ''))
    # トークンの検証
    email = confirm_verification_token(token)
    assert email == test_email

def test_confirm_verification_token_expired():
    from src.infrastructure.authentication.verification_token import confirm_verification_token
    test_email = "test@example.com"

    # トークンの生成
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY', 'test_secret_key'))
    token = serializer.dumps(test_email, salt=os.getenv('SECURITY_PASSWORD_SALT'))

    # トークンの有効期限を過ぎた場合の確認
    time.sleep(2)
    with pytest.raises(CredentialsError, match="Invalid token"):
        confirm_verification_token(token, expiration=1)

def test_confirm_verification_token_invalid():
    from src.infrastructure.authentication.verification_token import confirm_verification_token
    invalid_token = "invalidtoken"

    # 無効なトークンの確認
    with pytest.raises(CredentialsError, match="Invalid token"):
        confirm_verification_token(invalid_token)
