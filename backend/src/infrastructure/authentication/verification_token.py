# src/infrastracture/authentication/verification_token.py
import os
from itsdangerous import URLSafeTimedSerializer

from src.domain.exceptions.credentials_error import CredentialsError


SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
SALT = os.getenv("SECURITY_PASSWORD_SALT", "your_password_salt")

def generate_verification_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SALT)

def confirm_verification_token(token: str, expiration: int = 3600) -> str:
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt=SALT, max_age=expiration)
    except Exception:
        raise CredentialsError("Invalid token")
    return email
