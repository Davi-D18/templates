from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from {{ cookiecutter.project_slug }}.core.messages.users import (
    PASSWORD_MIN_LENGTH,
    USER_MIN_LENGTH,
)


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def username_min_length(cls, value: str) -> str:
        if len(value) < 4:
            raise ValueError(USER_MIN_LENGTH)
        return value

    @field_validator("password")
    @classmethod
    def password_min_length(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError(PASSWORD_MIN_LENGTH)
        return value


class UserUpdateSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    @field_validator("username")
    @classmethod
    def username_min_length(cls, value: str | None) -> str | None:
        if value is not None and len(value) < 4:
            raise ValueError(USER_MIN_LENGTH)
        return value

    @field_validator("password")
    @classmethod
    def password_min_length(cls, value: str | None) -> str | None:
        if value is not None and len(value) < 8:
            raise ValueError(PASSWORD_MIN_LENGTH)
        return value


class UserPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class UserListPublicSchema(BaseModel):
    users: list[UserPublicSchema]
