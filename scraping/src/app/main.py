from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from twisted.internet import reactor

from app.core.config import settings

from .schema.job import JobResponseDetailed, JobResponseSimple
from .schema.scrape import ScrapeRequest, ScrapeResponse


from .scrapers.spiders.bushcare import BushcareSpider
from .scrapers.spiders.midwest_herb import MidwestHerbariaSpider
from scrapy.crawler import CrawlerProcess
from .models.plant_scraped import ScrapedPlant



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
runner = CrawlerProcess(settings={
        'DOWNLOAD_DELAY': 3,
        'ROBOTSTXT_OBEY': False,
        'BOT_NAME': 'floraSpider',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
        'COOKIES_ENABLED': False
    })

async def run_spider(job_id):
    #TODO: figure how to find plants
    #TODO: before start create job for db with name
    #TODO: after crawl done, insert all to db, find plant and update job as done, else job as error
    try:
        plants = []
        #runner.crawl(BushcareSpider, plants=plants)
        runner.crawl(MidwestHerbariaSpider, plants=plants)
        runner.start()

        print('FOUND PLANTS: ', len(plants))
        plants = []
        for e in plants:
            await ScrapedPlant.create(**e)
    except Exception as e:
        print(e)
        pass


@app.post("/scrape", tags=["scraper"]) #TODO: finish endpoints, make counter for job_id
def scrape(scrape_req: ScrapeRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_spider, job_id=1)
    return {"job_id": 1}


@app.get("/job/{job_id}", tags=["jobs"])
async def job_simple(job_id: str):
    return await ScrapedPlant.all()


@app.get("/job/{job_id}/details", tags=["jobs"], response_model=JobResponseDetailed)
async def job_details(job_id: str):
    raise NotImplemented


@app.get("/")
def test():
    return {"a": "b"}
