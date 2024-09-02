
from fastapi import APIRouter, Depends, FastAPI, Form
from fastapi import Request
from fastapi.responses import HTMLResponse

from apps.template.auth_html import AUTH_HTML
from apps.auth.depends_auth_google import GoggleAuth
from apps.user.shemas import UserShemas

from .password import hash_password
from apps.user.dao import UserDAO

from .utils import encode_jwt, TokenInfo, get_current_active_auth_user, validate_user_login
from fastapi.security import HTTPBearer

# Create the auth appauthlib google register fastapi
auth_app = FastAPI()

http_bearer = HTTPBearer()

router = APIRouter(
    prefix='/auth',
    tags=["Auth & Пользователи"],
)


@auth_app.get('/')
async def root():
    return HTMLResponse(AUTH_HTML['welcome'])


@router.get('/register')
async def register(request: Request):
    return HTMLResponse(AUTH_HTML['register_good'])


@router.post('/register')
async def register_post(
        given_name: str = Form(...), family_name: str = Form(...),
        email: str = Form(...), password: str = Form(...)):
    try:
        hashed_password: str = await hash_password(password)
        await UserDAO.add_user(given_name, family_name, email, hashed_password)
        return HTMLResponse(AUTH_HTML['welcome_register'])
    except:  # noqa: E722
        return HTMLResponse(AUTH_HTML['register_good'])


@router.get('/register/google')
async def register_get_google(request: Request):
    redirect_uri: str = GoggleAuth.FRONTEND_URL
    return await GoggleAuth.oauth.google.authorize_redirect(
        request, redirect_uri
    )


@auth_app.get('/token')
async def auth(request: Request):
    access_token: str = \
        await GoggleAuth.oauth.google.authorize_access_token(request)
    userdata: dict = access_token['userinfo']
    await UserDAO.add_user(
        given_names=userdata.get("given_name"),
        family_names=userdata.get("family_name") or None,
        email=userdata.get("email"),
        password=userdata.get("at_hash")
    )
    return HTMLResponse(AUTH_HTML['welcome_register'])


@router.post('/login', response_model=TokenInfo)
async def login(user: UserShemas = Depends(validate_user_login)):
    token: str = await encode_jwt(
        {"sub": user.email,
         'given_name': user.given_name,
         'family_name': user.family_name}
    )
    return TokenInfo(
        access_token=token,
        token_type="bearer"
    )


@router.get('/users/me')
async def auth_user_check_self_info(
    user: UserShemas = Depends(get_current_active_auth_user),
):
    return {'given_name': user.given_name, 'family_name': user.family_name}


@auth_app.route(path='/login-google')
async def login_google(request: Request):
    redirect_uri: str = GoggleAuth.FRONTEND_URL
    return await GoggleAuth.oauth.google.authorize_redirect(
        request, redirect_uri
    )


@router.get("/check-email")
async def check_email(email_check):
    try:
        user = await UserDAO.get_user_by_email(email_check)
        if user.email:
            return {"exists": True}
    except:  # noqa: E722
        return {"exists": False}
