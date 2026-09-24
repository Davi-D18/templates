from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from {{ cookiecutter.project_slug }}.app.models.users import User
from {{ cookiecutter.project_slug }}.core.messages import jwt

from .database import get_session
from .security import JWTAuth, verify_password

security = HTTPBearer()


class Authentication:
    @staticmethod
    async def authenticate_user(email: str, password: str, db: AsyncSession):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password):
            return None

        return user

    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_session),
    ) -> User:
        payload = JWTAuth.verify_token(credentials.credentials)
        user_id_str = payload.get("sub")

        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=jwt.JWT_TOKEN_INVALID,
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            user_id = int(user_id_str)
        except (ValueError, TypeError) as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=jwt.JWT_TOKEN_INVALID,
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=jwt.JWT_TOKEN_INVALID,
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
