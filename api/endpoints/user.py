from fastapi import APIRouter, HTTPException
import crud.user
from schemas.user import UserAuth, TokenResponse, TokenPayload, EmailRequest
from models.user import User
from config.security import get_password_hash, create_access_token, create_refresh_token
from jose import jwt
from config.config import settings
from pydantic import ValidationError
from utils import email


router = APIRouter()


@router.post("/signup")
async def create_new_user(user: UserAuth):
    """
    Function to create new user
    :param user:
    :return:
    """
    user_exist = await crud.user.get_user_by_username(username=user.username)
    if user_exist:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    user_obj = User(
        username=user.username,
        password=get_password_hash(user.password)
    )

    new_user = await crud.user.create_user(user_obj)
    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(user: UserAuth):
    user_exist = await crud.user.authenticate(user_auth=user)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    res = TokenResponse(
        access_token=create_access_token(user_exist.user_id),
        refresh_token=create_refresh_token(user_exist.user_id)
    )
    return res


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_payload = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Invalid token",
        )

    user_exist = await crud.user.get_user_by_user_id(token_payload.sub)
    if not user_exist:
        raise HTTPException(
            status_code=404,
            detail="Invalid token for user",
        )

    res = TokenResponse(
        access_token=create_access_token(user_exist.id),
        refresh_token=create_refresh_token(user_exist.id)
    )
    return res
