from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist

from ..schema import plant
from ..utils.tasks import check_if_job_exists, scrape_for_plant

router = APIRouter()


@router.get(
    "/plant",
    tags=["plant"],
    response_model=List[plant.PlantOut_Pydantic],
    responses={403: {"detail": "Not authorized"}},
)
async def get_plants():
    return await plant.get_plants()


@router.get(
    "/plant/{latin_name}",
    tags=["plant"],
    response_model=plant.PlantOut_Pydantic,
    responses={
        404: {"detail": "Object does not exist"},
        403: {"detail": "Not authorized"},
    },
)
async def get_plant(
    latin_name: str,
    background_tasks: BackgroundTasks,
):
    try:
        return await plant.get_plant(latin_name)
    except DoesNotExist:
        if not await check_if_job_exists(latin_name):
            background_tasks.add_task(scrape_for_plant, latin_name)
            return JSONResponse(
                status_code=404, content={"detail": "Object does not exist"}
            )
        else:
            return await plant.get_plant(latin_name)


@router.post(
    "/plant",
    tags=["plant"],
    response_model=plant.PlantOut_Pydantic,
    responses={403: {"detail": "Not authorized"}},
)
async def create_plant(plant_in: plant.PlantIn_Pydantic):
    return await plant.create_plant(plant_in)


@router.put(
    "/plant/{latin_name}",
    tags=["plant"],
    response_model=plant.PlantOut_Pydantic,
    responses={403: {"detail": "Not authorized"}},
)
async def update_plant(latin_name: str, plant_in: plant.Plant_Update_Pydantic):
    return await plant.update_plant(latin_name, plant_in)
