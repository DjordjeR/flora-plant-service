from enum import Enum

from pydantic import BaseModel


class JobTypeEnum(str, Enum):
    done = "done"
    running = "running"
    stopped = "stopped"
    error = "error"


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
