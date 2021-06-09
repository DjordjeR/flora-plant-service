from fastapi import APIRouter
from typing import List
from ..schema import plant

router = APIRouter()

# TODO: Add pagination if needed
@router.get("/plant", tags=["plant"], response_model=List[plant.PlantOut_Pydantic])
async def get_plants():
    return await plant.get_plants()


@router.get(
    "/plant/{plant_name}", tags=["plant"], response_model=plant.PlantOut_Pydantic
)
async def get_plant(plant_name: str):
    return await plant.get_plant(plant_name)


@router.post("/plant", tags=["plant"], response_model=plant.PlantOut_Pydantic)
async def create_plant(plant_in: plant.PlantIn_Pydantic):
    return await plant.create_plant(plant_in)


@router.put(
    "/plant/{plant_name}", tags=["plant"], response_model=plant.PlantOut_Pydantic
)
async def update_plant(plant_name: str, plant_in: plant.PlantIn_Pydantic):
    return {"message": "Hello world!"}
