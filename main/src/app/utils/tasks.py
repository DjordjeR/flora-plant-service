# Some bacground tasks


from ..models.plant import PlantJob
from ..utils.scrape import Scrape
from ..models.plant import PlantJob


async def scrape_for_plant(plant_name: str):
    scaper = Scrape()
    job_id = await scaper.start_job(plant_name)
    await PlantJob.create(search_query=plant_name, job_id=job_id)
