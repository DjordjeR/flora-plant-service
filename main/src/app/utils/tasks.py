# Some bacground tasks

from tortoise.exceptions import DoesNotExist

from ..models.plant import PlantJob
from ..schema import plant
from ..utils.scrape import Scrape
from ..utils import search


async def check_if_job_exists(plant_name: str) -> bool:
    try:
        plant_job = await PlantJob.get(search_query=plant_name)
    except DoesNotExist:
        return False

    scraper = Scrape()
    try:
        data = await scraper.get_job(plant_job.id)
    except Exception:
        return False

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


async def scrape_for_plant(plant_name: str):
    try:
        scaper = Scrape()
        job_id = await scaper.start_job(plant_name)
        await PlantJob.create(search_query=plant_name, job_id=job_id)
    except Exception:
        # Nothing we can do in this case since its async task
        pass
