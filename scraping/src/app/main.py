from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from twisted.internet import reactor

from app.core.config import settings

from .schema.job import JobResponseDetailed, JobResponseSimple, ScrapedPlant_Pydantic
from .schema.scrape import ScrapeRequest, ScrapeResponse


from .scrapers.spiders.bushcare import BushcareSpider
from .scrapers.spiders.midwest_herb import MidwestHerbariaSpider
from scrapy.crawler import CrawlerProcess
from .models.plant_scraped import ScrapedPlant
from .models.job import ScrapeJob, JobTypeEnum



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

async def run_spider(job_id, plant_name):
    #TODO: figure how to find plants
    try:
        plants = []
        runner.crawl(BushcareSpider, plants=plants)
        #runner.crawl(MidwestHerbariaSpider, plants=plants)
        runner.start()
        print('AMOUNT OF FOUND PLANTS: ', len(plants))
        #plants = []
        once = True
        res = None
        for e in plants:
            if once:
                once = False
                res = await ScrapedPlant.get_or_create(**e)
        
        # after done with adding plants to scraperDB, lets mark job as done and return 
        
        print('*'*200)
        print(res[0])
        res_pyd = await ScrapedPlant_Pydantic.from_tortoise_orm(res[0])
        #TODO: update related job, if no plant found put ERROR, myb raise exception on search for plant_name and do it in exception
        related_job = await ScrapeJob.get(id=job_id)
        related_job.status = JobTypeEnum.done
        related_job.result = res_pyd.json()  #TODO: save corresponding plant from plant_name here, serialize pydantic ????
        await related_job.save()
        print('Job done!')
    except Exception as e:
        print('hehe')
        print(e)


@app.post("/scrape", tags=["scraper"]) #TODO: finish endpoints, make counter for job_id
async def scrape(scrape_req: ScrapeRequest, background_tasks: BackgroundTasks, response_model=ScrapeResponse):
    try:
        #TODO: create new job and background task only if task for same thing is not running already, BASE ON plant_name, somehow
        new_job = await ScrapeJob.get_or_create(status=JobTypeEnum.running, plant_name=scrape_req.plant_name, result="{ }")
        job_id = new_job[0].id
        print('Latest job ID=', job_id)        
        background_tasks.add_task(run_spider, job_id=job_id, plant_name=scrape_req.plant_name) #run scraping in background
        return ScrapeResponse(job_id=job_id)
    except Exception as e:
        print(e)
        return HTTPException(400, detail="Bad request")


@app.get("/job/{job_id}", tags=["jobs"])
async def job_simple(job_id: str, response_model=ScrapeJob):
    try:
        my_job = await ScrapeJob.get_or_none(id=job_id) #TODO: better way to write this ?
        if not my_job:
            return HTTPException(404, detail='Not found')
        return my_job
    except:
        return HTTPException(404, detail='Not found')


@app.get("/job/{job_id}/details", tags=["jobs"], response_model=JobResponseDetailed)
async def job_details(job_id: str):
    raise NotImplemented
