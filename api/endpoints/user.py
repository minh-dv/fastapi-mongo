from fastapi import APIRouter, HTTPException
import crud.user
from schemas.user import UserAuth, TokenResponse, TokenPayload, EmailRequest, ResetPassword
from models.user import User
from config.security import get_password_hash, create_access_token, create_refresh_token
from jose import jwt
from config.config import settings
from pydantic import ValidationError
from utils import email
import uuid


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


@router.post("/forgot-password")
async def forgot_password(request: EmailRequest):
    # Check exited user
    user = await crud.user.get_user_by_username(request.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create reset code and save it in database
    reset_code = str(uuid.uuid1())
    await crud.user.update_user(user.username, reset_code)

    # Sending email
    subject = "Testing Email For Dev."
    recipient = [request.username]
    message = """
    <!DOCTYPE html>
    <html>
    <title>Reset Password</title>
    <body>
    <div style="width:100%;font-family: monospace;">
        <h1>Hello, {0:}</h1>
        <p>Someone has requested a link to reset your password. If you requested this, you can change your password through the button below.</p>
        <a href="http://127.0.0.1:8000/user/reset-password?reset_password_token={1:}" style="box-sizing:border-box;border-color:#1f8feb;text-decoration:none;background-color:#1f8feb;border:solid 1px #1f8feb;border-radius:4px;color:#ffffff;font-size:16px;font-weight:bold;margin:0;padding:12px 24px;text-transform:capitalize;display:inline-block" target="_blank">Reset Your Password</a>
        <p>If you didn't request this, you can ignore this email.</p>
        <p>Your password won't change until you access the link above and create a new one.</p>
    </div>
    </body>
    </html>
    """.format(request.username, reset_code)
    await email.send_email(subject, recipient, message)

    return {
        "code": 200,
        "message": "We've sent an email with instructions to reset your password."
    }


@router.post("/reset-password")
async def reset_password(reset_password_token: str, request: ResetPassword):
    # Check valid reset password token
    reset_token = await crud.user.get_user_by_reset_token(reset_password_token)
    if not reset_token:
        raise HTTPException(status_code=404, detail="Reset password token has expired, please request a new one.")

    # Check both new & confirm password are matched
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=403, detail="New password is not match.")

    # Reset new password
    new_hash_password = get_password_hash(request.new_password)
    await crud.user.reset_password(new_hash_password, reset_token.username)

    # Disable reset code
    await crud.user.disable_reset_code(reset_password_token, reset_token.username)

    return {
        "code": 200,
        "message": "Password has been reset successfully"
    }