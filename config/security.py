from passlib.context import CryptContext
from jose import jwt
from datetime import timedelta, datetime
from config.config import settings
from typing import Union, Any


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "exp": expires,
        "sub": str(subject)
    }

    encode_jwt = jwt.encode(payload, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encode_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    payload = {
        "exp": expires,
        "sub": str(subject)
    }

    encode_jwt = jwt.encode(payload, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)
    return encode_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
