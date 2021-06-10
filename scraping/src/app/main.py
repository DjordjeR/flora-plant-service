from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings

from .schema.job import JobResponseDetailed, JobResponseSimple
from .schema.scrape import ScrapeRequest, ScrapeResponse


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_tortoise(
        _app,
        config=settings.TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    return _app


app = get_application()


@app.post("/scrape", tags=["scraper"], response_model=ScrapeResponse)
async def scrape(scrape_req: ScrapeRequest):
    raise NotImplemented


@app.get("/job/{job_id}", tags=["jobs"], response_model=JobResponseSimple)
async def job_simple(job_id: str):
    raise NotImplemented


@app.get("/job/{job_id}/details", tags=["jobs"], response_model=JobResponseDetailed)
async def job_details(job_id: str):
    raise NotImplemented


@app.get("/")
def test():
    return {"a": "b"}
