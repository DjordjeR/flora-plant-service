from typing import Optional
from fastapi import APIRouter
from starlette.background import BackgroundTasks

from ..utils import search as msearch
from ..schema.search import SearchResult
from ..utils.tasks import check_if_job_exists, scrape_for_plant

router = APIRouter()


async def _helper():

    if await check_if_job_exists(q):
        return ret
    else:
        background_tasks.add_task(scrape_for_plant, q)


@router.get("/search", tags=["search"], response_model=SearchResult)
async def search(
    q: str,
    background_tasks: BackgroundTasks,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
):
    opt_params = {
        "limit": limit,
        "offset": offset,
    }
    try:
        ret = msearch.search(q, opt_params)

        if ret.get("nbHits", 1) == 0:
            print("NO hits for this")
            if await check_if_job_exists(q):
                return SearchResult(**ret)
            else:
                background_tasks.add_task(scrape_for_plant, q)
        return SearchResult(**ret)
    except Exception:
        await check_if_job_exists(q)
        background_tasks.add_task(scrape_for_plant, q)
        return SearchResult(hits=[], offset=offset, limit=limit, nbHits=0, query=q)
