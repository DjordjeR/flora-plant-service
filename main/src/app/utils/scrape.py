import httpx


class Scrape:
    def __init__(self, base_url: str = "scraping_service:8080"):
        self._base_url = base_url

    async def _request(client: httpx.AsyncClient, path: str):
        response = await client.get(path)
        return response

    async def _task(self, path: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"self._base_url{path}")

        return response

    async def start_job(self):
        pass