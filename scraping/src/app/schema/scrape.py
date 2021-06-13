from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    search_query: str


class ScrapeResponse(BaseModel):
    job_id: int
