from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from {{ cookiecutter.project_slug }}.app.models.users import User
from {{ cookiecutter.project_slug }}.app.schemas.users import (
    UserListPublicSchema,
    UserPublicSchema,
    UserSchema,
    UserUpdateSchema,
)
from {{ cookiecutter.project_slug }}.core.configs.auth import Authentication
from {{ cookiecutter.project_slug }}.core.configs.database import get_session
from {{ cookiecutter.project_slug }}.core.configs.security import get_password_hash
from {{ cookiecutter.project_slug }}.core.messages.users import (
    EMAIL_EXISTS,
    USER_NOT_EXISTS,
    USERNAME_EXISTS,
)

router = APIRouter()


@router.post(
    "/",
    response_model=UserPublicSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo usuário",
)
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_session)):
    username_exists = await db.scalar(
        select(exists().where(User.username == user.username))
    )
    if username_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=USERNAME_EXISTS
        )

    email_exists = await db.scalar(select(exists().where(User.email == user.email)))
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=EMAIL_EXISTS
        )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserListPublicSchema,
    summary="Listar usuários",
)
async def list_users(
    offset: int = Query(0, ge=0, description="Registros para pular"),
    limit: int = Query(100, ge=1, le=100, description="Limite de registros"),
    search: str | None = Query(None, description="Busca por username ou email"),
    db: AsyncSession = Depends(get_session),
):
    query = select(User)

    if search:
        search_filter = f"%{search}%"
        query = query.where(
            (User.username.ilike(search_filter)) | (User.email.ilike(search_filter))
        )

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)

    return {"users": result.scalars().all(), "offset": offset, "limit": limit}


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserPublicSchema,
    summary="Buscar usuário por ID",
)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_EXISTS
        )

    return user


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserPublicSchema,
    summary="Atualizar usuário",
)
async def update_user(
    user_id: int,
    user_update: UserUpdateSchema,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(Authentication.get_current_user),
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_EXISTS
        )

    update_data = user_update.model_dump(exclude_unset=True)

    if "username" in update_data and update_data["username"] != user.username:
        username_exists = await db.scalar(
            select(
                exists().where(
                    (User.username == update_data["username"]) & (User.id != user_id)
                )
            )
        )
        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=USERNAME_EXISTS
            )

    if "email" in update_data and update_data["email"] != user.email:
        email_exists = await db.scalar(
            select(
                exists().where(
                    (User.email == update_data["email"]) & (User.id != user_id)
                )
            )
        )
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=EMAIL_EXISTS
            )

    if update_data.get("password"):
        update_data["password"] = get_password_hash(update_data["password"])

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar usuário",
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(Authentication.get_current_user),
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_EXISTS
        )

    await db.delete(user)
    await db.commit()
