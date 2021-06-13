import json
import httpx

from app.core.config import settings


class Scrape:
    def __init__(self, base_url: str = settings.SCRAPING_URL):
        self._base_url = base_url
        if not self._base_url.endswith("/"):
            self._base_url += "/"

        self._scrape_url = self._base_url + "scrape"
        self._job_url = self._base_url + "job"

    async def _request_scrape(self, payload: dict) -> dict:
        async with httpx.AsyncClient() as client:
            print(self._scrape_url)
            print(payload)
            r = await client.post(
                self._scrape_url,
                json=payload,
            )
        return r.json()

    async def _get_job_details(self, job_id: int):
        async with httpx.AsyncClient() as client:
            r = await client.get(self._job_url + f"/{job_id}")
        return r.json()

    async def start_job(self, param: str) -> int:
        """Start scraping job on scraping service

        Args:
            param (str): search_query for scraping

        Returns:
            int: scraping job, so we can check details later
        """
        payload = {"search_query": param}
        json_data = await self._request_scrape(payload)
        return json_data["job_id"]

    async def get_job(self, job_id: int) -> dict:
        """Retreieve details about started job

        Args:
            job_id (int): id of the started job

        Returns:
            dict: result of the started job
        """
        return await self._get_job_details(job_id)