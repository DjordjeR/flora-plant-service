from pydantic import BaseModel

USERS = list()


class UserBase(BaseModel):
    username: str
    firstName: str
    lastName: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int


class UserDb(UserBase):
    id: int
    password: str


# Fake register user
async def register_user(user_in: UserIn) -> UserDb:
    user_saved = UserDb(id=len(USERS), **user_in.dict())
    USERS.append(user_saved)
    return user_saved
