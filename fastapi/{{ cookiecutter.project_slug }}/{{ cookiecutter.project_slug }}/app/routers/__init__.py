from fastapi import APIRouter

{% if cookiecutter.use_authentication == "yes" %}from .auth import router as auth_router
{% endif %}from .health import router as health_router
{% if cookiecutter.use_authentication == "yes" %}from .users import router as user_router
{% endif %}
api_router = APIRouter()
api_router.include_router(health_router)
{% if cookiecutter.use_authentication == "yes" %}api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
{% endif %}
