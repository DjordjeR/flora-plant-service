from enum import Enum
from ..models.plant_scraped import ScrapedPlant

from pydantic import BaseModel
from tortoise.contrib.pydantic.creator import pydantic_model_creator


class JobTypeEnum(str, Enum):
    done = "done"
    running = "running"
    stopped = "stopped"
    error = "error"

ScrapedPlant_Pydantic = pydantic_model_creator(ScrapedPlant)

# TODO: I have not idea what job result will be
class JobResult(BaseModel):
    result: str
    plant_info: str


class JobResponseSimple(BaseModel):
    job_id: int
    status: JobTypeEnum


class JobResponseDetailed(JobResponseSimple):
    job_id: int
    status: JobTypeEnum
    job_result: JobResult
