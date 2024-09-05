from fastapi import Depends, Form
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

from apps.auth.jwt import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    decode_jwt,
)
from apps.auth.password import check_password
from apps.depends.exception_user_auth import (
    IncorrectAccessTokenException,
    IncorrectPasswordException,
    IncorrectTokenException,
    NotActiveException,
    NotUserException,
)
from apps.user.dao import UserDAO
from apps.user.models import User
from apps.user.shemas import UserShemas

http_bearer = HTTPBearer()


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
    credentials: HTTPBasicCredentials = Depends(http_bearer),
) -> UserShemas:
    token = credentials.credentials
    try:
        payload = await decode_jwt(token=token)
    except InvalidTokenError:
        raise IncorrectTokenException()
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserShemas:
    return await get_current_auth_data(type_token=ACCESS_TOKEN_TYPE, payload=payload)


async def get_current_auth_refresh_token(
    payload: dict = Depends(get_current_token_payload),
) -> UserShemas:
    return await get_current_auth_data(ype_token=REFRESH_TOKEN_TYPE, payload=payload)


async def get_current_active_auth_user(
    user: UserShemas = Depends(get_current_auth_user),
) -> UserShemas:
    user_data = await UserDAO.get_user_by_email(email=user.email)
    if user_data is None:
        raise IncorrectTokenException()
    return user_data


async def get_current_auth_data(
    type_token: str,
    payload: dict = Depends(get_current_token_payload),
) -> UserShemas:
    token_type: str = payload.get(TOKEN_TYPE_FIELD)
    if token_type != type_token:
        raise IncorrectAccessTokenException()
    email: str | None = payload.get("sub")
    user_data = await UserDAO.get_user_by_email(email=email)
    if user_data is None:
        raise IncorrectTokenException()
    return user_data
