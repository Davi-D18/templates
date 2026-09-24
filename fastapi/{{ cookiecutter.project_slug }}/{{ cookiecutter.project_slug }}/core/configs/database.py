from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from {{ cookiecutter.project_slug }}.core.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)


class BaseModel(DeclarativeBase):
    pass


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
