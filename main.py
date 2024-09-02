import logging
import uvicorn
from fastapi import FastAPI

from apps.auth.auth import auth_app
from apps.auth.auth import router as router_users
from starlette.middleware.sessions import SessionMiddleware

from apps.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


app.include_router(router_users)

app.mount('/', auth_app)


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
