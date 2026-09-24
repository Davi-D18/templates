from pydantic import BaseModel, EmailStr, field_validator

from {{ cookiecutter.project_slug }}.core.messages import users


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError(users.PASSWORD_MIN_LENGTH)
        return value
