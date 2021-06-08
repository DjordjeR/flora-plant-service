from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["example"])
async def get_message():
    return {"message": "Hello world!"}
