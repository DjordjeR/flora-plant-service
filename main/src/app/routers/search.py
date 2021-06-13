from typing import Optional
from fastapi import APIRouter

from ..utils import search as msearch

router = APIRouter()


@router.get("/search", tags=["search"])
async def search(
    q: str,
    filters: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
):
    return msearch.search(q)
