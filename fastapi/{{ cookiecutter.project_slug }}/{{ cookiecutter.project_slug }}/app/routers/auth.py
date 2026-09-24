from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from {{ cookiecutter.project_slug }}.app.schemas.auth import LoginRequest, Token
from {{ cookiecutter.project_slug }}.core.configs.auth import Authentication
from {{ cookiecutter.project_slug }}.core.configs.database import get_session
from {{ cookiecutter.project_slug }}.core.configs.security import JWTAuth

router = APIRouter()


@router.post("/login", response_model=Token, summary="Login (JWT)")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_session)):
    user = await Authentication.authenticate_user(payload.email, payload.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = JWTAuth.create_access_token({"sub": str(user.id)})
    return Token(access_token=token, token_type="bearer")
