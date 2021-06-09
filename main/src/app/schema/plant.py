from typing import List
from tortoise.contrib.pydantic import pydantic_model_creator
from ..models import plant


PlantIn_Pydantic = pydantic_model_creator(
    plant.Plant, name="Plant", exclude_readonly=True
)
PlantOut_Pydantic = pydantic_model_creator(plant.Plant, name="Plant")


async def create_plant(plant_in: PlantIn_Pydantic) -> PlantOut_Pydantic:
    plant_obj = await plant.Plant.create(**plant_in.dict(exclude_unset=True))
    return await PlantOut_Pydantic.from_tortoise_orm(plant_obj)


async def get_plant(plant_name: str) -> PlantOut_Pydantic:    
    return await plant.Plant.get(common_name=plant_name)


async def get_plants() -> List[PlantOut_Pydantic]:
    return await plant.Plant.all()
