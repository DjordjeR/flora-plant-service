import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Depends
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings

from .authentication import auth_router, get_current_user
from .routers import example, plant, search


def _get_deps():
    if settings.AUTH_ON:
        return [Depends(get_current_user)]
    else:
        []


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(plant.router, dependencies=_get_deps())
    _app.include_router(auth_router)
    _app.include_router(search.router)
    register_tortoise(
        _app,
        config=settings.TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    return _app


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, port=8080, loop="asyncio", lifespan="on")
