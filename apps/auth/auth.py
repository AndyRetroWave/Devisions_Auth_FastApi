from fastapi import APIRouter, Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer

from apps.auth.depends_auth_google import GoggleAuth
from apps.depends.exception_user_auth import (
    IncorrectInputEmailException,
    IncorrectInputPasswordException,
)
from apps.template.auth_html import AUTH_HTML
from apps.user.dao import UserDAO
from apps.user.shemas import UserShemas

from .jwt import TokenInfo, create_access_token, create_refresh_token
from .password import hash_password
from .validation import (
    get_current_active_auth_user,
    get_current_auth_refresh_token,
    validate_user_login,
)

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
    hashed_password: str | bool = await hash_password(password)
    if hashed_password is False:
        raise IncorrectInputPasswordException()
    if await UserDAO.add_user(given_name, family_name, email, hashed_password) is None:
        raise IncorrectInputEmailException()
    return HTMLResponse(AUTH_HTML["welcome_register"])


# except:  # noqa: E722
#     return HTMLResponse(AUTH_HTML["register_good"])


@router.get("/register/google")
async def register_get_google(request: Request):
    redirect_uri: str = GoggleAuth.FRONTEND_URL
    return await GoggleAuth.oauth.google.authorize_redirect(request, redirect_uri)


@auth_app.get("/token")
async def auth(request: Request):
    access_token: str = await GoggleAuth.oauth.google.authorize_access_token(request)
    userdata: dict = access_token["userinfo"]
    await UserDAO.add_user(
        given_names=userdata.get("given_name"),
        family_names=userdata.get("family_name") or None,
        email=userdata.get("email"),
        password=userdata.get("at_hash"),
    )
    return RedirectResponse(url="/welcome", status_code=303)


@router.get("/login")
async def get_login(request: Request):
    return HTMLResponse(AUTH_HTML["login"])


@router.post("/login", response_model=TokenInfo)
async def post_login(user: UserShemas = Depends(validate_user_login)):
    acces_token: str = await create_access_token(user)
    refresh_token: str = await create_refresh_token(user)
    return TokenInfo(
        access_token=acces_token,
        refresh_token=refresh_token,
    )


@router.get("/register/google")
async def login_get_google(request: Request):
    redirect_uri: str = GoggleAuth.FRONTEND_URL
    return await GoggleAuth.oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/users/me")
async def auth_user_check_self_info(
    user: UserShemas = Depends(get_current_active_auth_user),
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
async def check_email(email_check: str):
    try:
        user = await UserDAO.get_user_by_email(email_check)
        if user.email:
            return {"exists": True}
    except:  # noqa: E722
        return {"exists": False}


@router.post("/refresh", response_model=TokenInfo)
async def auth_refresh_token(
    user: UserShemas = Depends(get_current_auth_refresh_token),
):
    access_token = await create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )
