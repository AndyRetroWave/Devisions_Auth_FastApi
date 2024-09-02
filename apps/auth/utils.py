from datetime import datetime, timedelta
from pathlib import Path
import aiofiles
from fastapi import Depends, Form
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from apps.auth.password import check_password
from apps.config import settings
from apps.depends.exception import (
    IncorrectPasswordException, IncorrectTokenException, NotActiveException,
    NotUserException
)
from apps.user.dao import UserDAO
from apps.user.models import User
from apps.user.shemas import UserShemas

from fastapi.security import (
    HTTPBearer, HTTPBasicCredentials)


http_bearer = HTTPBearer()


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


async def read_key(path: Path) -> str:
    async with aiofiles.open(path, mode='r') as f:
        return await f.read()


async def encode_jwt(
    payload: dict,
    algorithm: str = settings.AUTH_JWT.algorithm,
    expire_minutes: int = settings.AUTH_JWT.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire: str = now + expire_timedelta
    else:
        expire: str = now + timedelta(minutes=expire_minutes)
    to_encode.update({
        "exp": expire,
        'iat': now
    })
    private_key = await read_key(settings.AUTH_JWT.private_key_path)
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )
    return encoded


async def decode_jwt(
        token: str | bytes,
        algorithm: str = settings.AUTH_JWT.algorithm):
    public_key = await read_key(settings.AUTH_JWT.public_key_path)
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )
    return decoded


async def validate_user_login(email: str = Form(), password: str = Form()) -> User:
    user: User = await UserDAO.get_user_by_email(email=email)
    if user is None:
        raise NotUserException()
    valid_pass: bool = await check_password(password, user.hashed_password)
    if not valid_pass:
        raise IncorrectPasswordException()
    if user.is_active:
        return user
    raise NotActiveException()


async def get_current_token_payload(
        credentials: HTTPBasicCredentials = Depends(http_bearer)) -> UserShemas:
    token = credentials.credentials
    print(token)
    try:
        payload = await decode_jwt(
            token=token
        )
    except InvalidTokenError:
        raise IncorrectTokenException()
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload)
) -> UserShemas:
    email: str | None = payload.get('sub')
    user_data = await UserDAO.get_user_by_email(email=email)
    print(user_data)
    if user_data is None:
        raise IncorrectTokenException()
    return user_data


async def get_current_active_auth_user(
        user: UserShemas = Depends(get_current_token_payload)) -> UserShemas:
    user_data = await UserDAO.get_user_by_email(email=user['sub'])
    if user_data is None:
        raise IncorrectTokenException()
    return user_data
