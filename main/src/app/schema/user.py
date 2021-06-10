from pydantic import BaseModel
from pydantic.types import UUID4


class UserLoginResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str
    token_type: str
    session_state: str
    scope: str


class UserLoggedIn(BaseModel):
    sub: UUID4
    email_verified: bool
    name: str
    preferred_username: str
    email: str


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserKeycloackDetail(BaseModel):
    detail: str


class UserBase(BaseModel):
    username: str
    firstName: str
    lastName: str
    email: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: UUID4
