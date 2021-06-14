from typing import List
from pydantic import BaseModel
from .plant import PlantOut_Pydantic


class SearchResult(BaseModel):
    hits: List[PlantOut_Pydantic]
    offset: int
    limit: int
    query: str
    nbHits: int
