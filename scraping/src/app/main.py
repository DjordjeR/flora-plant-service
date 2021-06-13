import asyncio
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.core.config import settings

from .schema.job import ScrapedJob_Pydantic, ScrapedPlant_Pydantic
from .schema.scrape import ScrapeRequest, ScrapeResponse


from .scrapers.spiders.bushcare import BushcareSpider
from .scrapers.spiders.midwest_herb import MidwestHerbariaSpider
from scrapy.crawler import CrawlerProcess
from .models.plant_scraped import ScrapedPlant
from .models.job import ScrapeJob, JobTypeEnum

from fuzzywuzzy import fuzz
from multiprocessing import Process, Queue

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
        'ROBOTSTXT_OBEY': True,
        'BOT_NAME': 'floraSpider',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
        'COOKIES_ENABLED': False,
        'LOG_LEVEL': 'ERROR'
    })

def _execute_spider_in_process(q):
    plants = []
    plants_2 = []
    #runner.crawl(BushcareSpider, plants=plants)
    runner.crawl(MidwestHerbariaSpider, plants=plants_2)
    runner.start()
    plants.extend(plants_2)
    q.put(plants)


async def run_spider(job_id, search_query):
    plants = []
    q = Queue() # may god help you 
    p = Process(target=_execute_spider_in_process, args=(q,))
    p.start()
    loop = asyncio.get_event_loop()
    plants =  await loop.run_in_executor(None, q.get)
    await loop.run_in_executor(None, p.join)

    print('AMOUNT OF FOUND PLANTS: ', len(plants))
    matched_plants = set()
    for e in plants:
        ln = e.get('latin_name', '')
        del e['latin_name']
        res_awaited = await ScrapedPlant.get_or_create(latin_name=ln, defaults=e)
        res = res_awaited[0]
        ratios = [fuzz.token_set_ratio(cn, search_query) for cn in res.common_names]
        ratios.append(fuzz.token_set_ratio(res.latin_name, search_query))
        max_ratio = max(ratios)
        if max_ratio >= 80:
            print('Found fuzzy match of {}%'.format(max_ratio))
            matched_plants.add(res)

    # after done with adding plants to scraperDB, lets mark job as done and return
    print('*'*200)
    print('Amount of matched plants ', len(matched_plants))
    print('*'*200)

    #res_pyd = await ScrapedPlant_Pydantic.from_tortoise_orm(res[0])
    #TODO: update related job, if no plant found put ERROR, myb raise exception on search for plant_name and do it in exception
    related_job = await ScrapeJob.get(id=job_id)
    related_job.status = JobTypeEnum.done
    for e in matched_plants:
        e_pyd =  await ScrapedPlant_Pydantic.from_tortoise_orm(e)
        related_job.result.append(e_pyd.dict())
    #related_job.result = res_pyd.json()
    await related_job.save()
    print('Job done!')


@app.post("/scrape", tags=["scraper"], response_model=ScrapeResponse, responses={400: {"detail": "Bad request"}})
async def scrape(scrape_req: ScrapeRequest, background_tasks: BackgroundTasks):
    try:
        # check if similar plant name already in db, else checkif background tasks running

        #TODO: create new job and background task only if task for same thing is not running already, BASE ON plant_name, somehow
        # if task running and fuzzymatch >=80% then dont create background
        # if task ERROR then return cannot find data
        new_job = await ScrapeJob.get_or_create(status=JobTypeEnum.running, search_query=scrape_req.search_query)
        job_id = new_job[0].id
        print('Latest job ID=', job_id) 
        background_tasks.add_task(run_spider, job_id=job_id, search_query=scrape_req.search_query) #run scraping in background
        return ScrapeResponse(job_id=job_id)
    except Exception as e:
        print(e)
        return HTTPException(400, detail="Bad request")


@app.get("/job/{job_id}", tags=["jobs"], response_model=ScrapedJob_Pydantic, responses={404: {"detail": "Object does not exist"}})
async def job(job_id: int):
    my_job = await ScrapeJob.get(id=job_id)
    return await ScrapedJob_Pydantic.from_tortoise_orm(my_job)