from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    plant_name: str


class ScrapeResponse(BaseModel):
    job_id: int
