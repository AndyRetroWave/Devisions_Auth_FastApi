import logging
import uvicorn
from fastapi import FastAPI, Request

from apps.auth.api import api_app
from apps.auth.auth import auth_app
from apps.auth.auth import router as router_users
from starlette.middleware.sessions import SessionMiddleware
from apps.auth.depends_auth_google import GoggleAuth
from apps.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


@app.get('/register/google')
async def register_get_google(request: Request):
    redirect_uri = GoggleAuth.FRONTEND_URL
    return await GoggleAuth.oauth.google.authorize_redirect(request, redirect_uri)


@app.get('/token')
async def auth(request: Request):
    try:
        # Получение access_token от Google OAuth
        access_token = await GoggleAuth.oauth.google.authorize_access_token(request)
        logger.info(
            f"Access token received: {access_token.get('access_token')}")
        return {"access_token": access_token.get('access_token')}
    except Exception as e:
        logger.error(f"Error during OAuth authentication: {e}")
        raise HTTPException(status_code=400, detail=str(e))
app.include_router(router_users)

app.mount('/', auth_app)
app.mount('/api', api_app)


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
