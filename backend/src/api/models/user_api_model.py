from pydantic import BaseModel


class UserCreateModel(BaseModel):
    email: str
    password: str
    name: str

class UserReadModel(BaseModel):
    id: int
    email: str
    name: str
