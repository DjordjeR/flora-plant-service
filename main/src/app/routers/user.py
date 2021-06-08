from fastapi import APIRouter
from ..models import user


router = APIRouter()


@router.post("/user/login", tags=["user"])
async def user_login():
    return {"message": "user_login!"}


@router.get("/user/logout", tags=["user"])
async def user_logout():
    return {"message": "user_logout!"}


@router.post("/user/register", tags=["user"], response_model=user.UserOut)
async def user_register(user_in: user.UserIn):
    # TODO: Register user
    return await user.register_user(user_in)
