from fastapi import APIRouter

router = APIRouter()


@router.get("/plant/{plant_name}", tags=["plant"])
async def get_plant(plant_name):
    return {"message": "Hello world!"}


@router.post("/plant/{plant_name}", tags=["plant"])
async def create_plant(plant_name):
    return {"message": "Hello world!"}


@router.put("/plant/{plant_name}", tags=["plant"])
async def update_plant(plant_name):
    return {"message": "Hello world!"}
