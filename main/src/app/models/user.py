from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
    password: str


class UserRegisterResponse(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
