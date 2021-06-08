from fastapi.param_functions import Depends
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from .routers import example, user, search, plant


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(example.router)
    _app.include_router(plant.router)
    _app.include_router(user.router)
    _app.include_router(search.router)

    return _app


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, port=8080, loop="asyncio")
