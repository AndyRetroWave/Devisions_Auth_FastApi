from fastapi import APIRouter, FastAPI, Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from apps.template.auth_html import AUTH_HTML
from apps.auth.depends_auth_google import GoggleAuth

# Create the auth appauthlib google register fastapi
auth_app = FastAPI()

router = APIRouter(
    prefix='/auth',
    tags=["Auth & Пользователи"],
)


@auth_app.get('/')
async def root():
    return HTMLResponse(AUTH_HTML['welcome'])


@router.get('/register')
async def register(request: Request):
    return HTMLResponse(AUTH_HTML['register'])


@router.post('/register')
async def register_post(
        given_name: str = Form(...), family_name: str = Form(...),
        email: str = Form(...), password: str = Form(...)):

    return HTMLResponse(given_name)


@auth_app.route('/login')
async def login(request: Request):
    # This creates the url for our /auth endpoint
    redirect_uri = GoggleAuth.FRONTEND_URL
    return await GoggleAuth.oauth.google.authorize_redirect(request, redirect_uri)
