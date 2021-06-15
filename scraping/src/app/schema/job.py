from enum import Enum
from ..models.job import ScrapeJob
from ..models.plant_scraped import ScrapedPlant

from pydantic import BaseModel
from tortoise.contrib.pydantic.creator import pydantic_model_creator


class JobTypeEnum(str, Enum):
    done = "done"
    running = "running"
    stopped = "stopped"
    error = "error"

ScrapedPlant_Pydantic = pydantic_model_creator(ScrapedPlant, exclude=("id",))
ScrapedJob_Pydantic = pydantic_model_creator(ScrapeJob)
