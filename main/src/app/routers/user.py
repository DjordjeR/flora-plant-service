from fastapi import APIRouter
from ..models import user


router = APIRouter()


@router.post("/user/login", tags=["user"])
async def user_login():
    return {"message": "user_logout!"}


@router.get("/user/logout", tags=["user"])
async def user_logout():
    return {"message": "user_logout!"}


@router.post("/user/register", tags=["user"], response_model=user.UserRegisterResponse)
async def user_register():
    return {"message": "user_register!"}
