from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import List
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist

from ..schema import plant
from ..utils.tasks import scrape_for_plant
from ..models.plant import PlantJob
from ..utils.scrape import Scrape

from ..utils import search

router = APIRouter()

# TODO: Add pagination if needed
@router.get("/plant", tags=["plant"], response_model=List[plant.PlantOut_Pydantic])
async def get_plants():
    return await plant.get_plants()


async def _check_if_job_exists(plant_name: str):
    # TODO: Add this stuff to search too
    try:
        plant_job = await PlantJob.get(search_query=plant_name)
    except DoesNotExist:
        return None

    scraper = Scrape()
    try:
        data = await scraper.get_job(plant_job.id)
    except Exception:
        return None

    if data.get("status") == "done":
        for p in data.get("result"):
            p_new = plant.PlantIn_Pydantic(
                latin_name=p["latin_name"],
                common_name=p["common_names"],
                metadata=p["additional"],
            )
            plant_out = await plant.get_or_create(p_new)
            search.update_or_add_plant(plant_out)
        await PlantJob.delete(plant_job)

    return True


@router.get(
    "/plant/{plant_name}",
    tags=["plant"],
    response_model=plant.PlantOut_Pydantic,
    responses={404: {"detail": "Object does not exist"}},
)
async def get_plant(plant_name: str, background_tasks: BackgroundTasks):
    try:
        return await plant.get_plant(plant_name)
    except DoesNotExist:
        exists = await _check_if_job_exists(plant_name)
        if not exists:
            background_tasks.add_task(scrape_for_plant, plant_name)
            return JSONResponse(
                status_code=404, content={"detail": "Object does not exist"}
            )
        else:
            return await plant.get_plant(plant_name)


@router.post("/plant", tags=["plant"], response_model=plant.PlantOut_Pydantic)
async def create_plant(plant_in: plant.PlantIn_Pydantic):
    return await plant.create_plant(plant_in)


@router.put(
    "/plant/{plant_name}", tags=["plant"], response_model=plant.PlantOut_Pydantic
)
async def update_plant(plant_name: str, plant_in: plant.Plant_Update_Pydantic):
    return await plant.update_plant(plant_name, plant_in)
