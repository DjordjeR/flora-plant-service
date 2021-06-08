from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["main"])
async def get_message():
    return {"message": "Hello world!"}
