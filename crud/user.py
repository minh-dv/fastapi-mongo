from models.user import User
from schemas.user import UserAuth
from typing import Optional
from fastapi import HTTPException
from config.security import verify_password
from uuid import UUID


async def get_user_by_username(username: str) -> User:
    try:
        user = await User.find_one(User.username == username)
        return user
    except Exception as err:
        raise err


async def update_user(username: str, reset_code: str) -> User:
    try:
        user = await User.find_one(User.username == username)
        update_query = {"$set": {
            "reset_code": reset_code
        }}
        await user.update(update_query)
        return user
    except Exception as err:
        raise err


async def get_user_by_user_id(user_id: UUID) -> Optional[User]:
    try:
        user = await User.find_one(User.user_id == user_id)
        return user
    except Exception as err:
        raise err


async def create_user(user: User) -> User:
    try:
        new_user = await user.create()
        return new_user
    except Exception as err:
        raise err


async def authenticate(user_auth: UserAuth) -> Optional[User]:
    try:
        user_exist = await get_user_by_username(user_auth.username)
        if not user_exist:
            raise HTTPException(
                status_code=403,
                detail="Incorrect email or password"
            )
        if not verify_password(user_auth.password, user_exist.password):
            raise HTTPException(
                status_code=403,
                detail="Incorrect email or password"
            )

        return user_exist

    except Exception as err:
        raise err


async def get_user_by_reset_token(reset_token: str) -> User:
    try:
        user = await User.find_one(User.reset_code == reset_token)
        return user
    except Exception as err:
        raise err


async def reset_password(new_hash_password: str, username: str):
    try:
        user = await User.find_one(User.username == username)
        update_query = {"$set": {
            "password": new_hash_password
        }}
        await user.update(update_query)
        return user
    except Exception as err:
        raise err


async def disable_reset_code(reset_password_token: str, username: str):
    try:
        user = await User.find_one(User.username == username)
        update_query = {"$set": {
            "reset_code": None
        }}
        await user.update(update_query)
        return user
    except Exception as err:
        raise err

