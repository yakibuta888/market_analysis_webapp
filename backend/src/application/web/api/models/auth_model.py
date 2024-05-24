# src/application/web/api/models/auth_model.py
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class LoginModel(BaseModel):
    email: str
    password: str
