from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from core import settings, routes, constants


def get_application() -> FastAPI:
    setting = settings.AppSettings()

    application = FastAPI(**setting.fastapi_kwargs)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=setting.allowed_hosts,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    application.include_router(routes.router, prefix=setting.api_prefix)

    register_tortoise(
        application,
        config=constants.TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )

    return application

app = get_application()

@app.get("/")
async def root():
    return {"message": "Hello World"}

