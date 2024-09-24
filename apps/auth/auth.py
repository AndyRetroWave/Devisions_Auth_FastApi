from typing import Any, Literal

from fastapi import APIRouter, Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer

from apps.auth.depends_auth_google import GoggleAuth
from apps.auth.services_auth import TokenAuthValidate
from apps.template.auth_html import AUTH_HTML
from apps.user.dao import UserDAO
from apps.user.models import User
from apps.user.shemas import UserShemas

from .jwt import (
    CreateTokenPayload,
    TokenInfo,
)
from .password import hash_password
from .services_auth import GetTokenType

# Create the auth appauthlib google register fastapi
auth_app = FastAPI()

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
    dependencies=[Depends(http_bearer)],
)


@auth_app.get("/")
async def root():
    return HTMLResponse(AUTH_HTML["welcome"])


@auth_app.get("/welcome")
async def good_reguster():
    return HTMLResponse(AUTH_HTML["welcome_register"])


@router.get("/register")
async def get_register(request: Request):
    return HTMLResponse(AUTH_HTML["register_good"])


@router.post("/register")
async def post_register(
    given_name: str = Form(...),
    family_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    hashed_password = await hash_password(password)
    await UserDAO.add_user(given_name, family_name, email, hashed_password) is None
    return HTMLResponse(AUTH_HTML["welcome_register"])


@router.get("/register/google")
async def register_get_google(request: Request):
    redirect_uri: str = GoggleAuth.FRONTEND_URL
    return await GoggleAuth.oauth.google.authorize_redirect(request, redirect_uri)


@auth_app.get("/token")
async def auth(request: Request) -> RedirectResponse:
    access_token: dict = await GoggleAuth.oauth.google.authorize_access_token(request)
    userdata: dict[str, Any] = access_token["userinfo"]
    given_name: str | None = userdata.get("given_name")
    family_name: str | None = userdata.get("family_name")
    email: str | None = userdata.get("email")
    at_hash: str | None = userdata.get("at_hash")
    await UserDAO.add_user(
        given_names=given_name,  # type: ignore
        family_names=family_name,  # type: ignore
        email=email,  # type: ignore
        password=at_hash,  # type: ignore
    )
    return RedirectResponse(url="/welcome", status_code=303)


@router.get("/login")
async def get_login(request: Request):
    return HTMLResponse(AUTH_HTML["login"])


@router.post("/login", response_model=TokenInfo)
async def post_login(user: UserShemas = Depends(TokenAuthValidate.validate_user_login)):
    accession: str = await CreateTokenPayload.create_access_token(user)
    refresh_token: str = await CreateTokenPayload.create_refresh_token(user)
    return TokenInfo(
        access_token=accession,
        refresh_token=refresh_token,
    )


@router.get("/users/me")
async def auth_user_check_self_info(
    user: UserShemas = Depends(GetTokenType.get_current_active_auth_user),
):
    return {
        "given_name": user.given_name,
        "family_name": user.family_name,
    }


@router.get(path="/login/google")
async def login_google(request: Request):
    redirect_uri: str = GoggleAuth.FRONTEND_URL
    return await GoggleAuth.oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/check-email")
async def check_email(email_check: str) -> dict[Literal["exists"], bool]:
    try:
        user: User = await UserDAO.get_user_by_email(email_check)  # type: ignore
        if user.email:
            return {"exists": True}
    except:  # noqa: E722
        return {"exists": False}


@router.post("/refresh", response_model=TokenInfo)
async def auth_refresh_token(
    user: UserShemas = Depends(GetTokenType.get_current_auth_refresh_token),
):
    access_token: str = await CreateTokenPayload.create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )
