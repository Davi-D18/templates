from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from {{ cookiecutter.project_slug }}.app.routers import api_router
from {{ cookiecutter.project_slug }}.core.settings import settings


def create_app() -> FastAPI:
    """Cria a aplicação FastAPI com routers e middlewares."""
    app = FastAPI(
        title={{ cookiecutter.project_name | tojson }},
        version={{ cookiecutter.version | tojson }},
        description={{ cookiecutter.description | tojson }},
{%- if cookiecutter.use_documentation == "no" %}
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
{%- endif %}
    )

    cors_origins = [
        origin.strip()
        for origin in getattr(settings, "CORS_ORIGINS", "").split(",")
        if origin.strip()
    ]
    if cors_origins:
        cors_methods = [
            method.strip()
            for method in getattr(settings, "CORS_METHODS", "*").split(",")
            if method.strip()
        ]
        cors_headers = [
            header.strip()
            for header in getattr(settings, "CORS_HEADERS", "*").split(",")
            if header.strip()
        ]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_methods=cors_methods or ["*"],
            allow_headers=cors_headers or ["*"],
        )

    app.include_router(api_router)
    return app
