from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserAuth(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "test",
                "password": "123123"
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: UUID = None
    exp: int = None


class EmailRequest(BaseModel):
    username: EmailStr


class ResetPassword(BaseModel):
    new_password: str
    confirm_password: str
