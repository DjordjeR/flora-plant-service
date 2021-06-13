from typing import List
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import DoesNotExist
from ..models import plant


PlantIn_Pydantic = pydantic_model_creator(
    plant.Plant, name="Plant", exclude_readonly=True
)
PlantOut_Pydantic = pydantic_model_creator(plant.Plant, name="Plant")

Plant_Update_Pydantic = pydantic_model_creator(
    plant.Plant,
    exclude_readonly=True,
    name="PlantUpdate",
    exclude=["latin_name"],
)


async def create_plant(plant_in: PlantIn_Pydantic) -> PlantOut_Pydantic:
    plant_obj = await plant.Plant.create(**plant_in.dict(exclude_unset=True))
    return await PlantOut_Pydantic.from_tortoise_orm(plant_obj)


async def get_plant(plant_name: str) -> PlantOut_Pydantic:
    found_plant = await plant.Plant.get(latin_name=plant_name)
    return found_plant


async def get_plants() -> List[PlantOut_Pydantic]:
    return await plant.Plant.all()


async def update_plant(
    plant_name: str, plant_in: Plant_Update_Pydantic
) -> PlantOut_Pydantic:
    plant_obj = await plant.Plant.get(latin_name=plant_name)
    plant_obj.metadata = plant_in.metadata
    await plant_obj.save(update_fields=["metadata"])
    return await PlantOut_Pydantic.from_tortoise_orm(plant_obj)
