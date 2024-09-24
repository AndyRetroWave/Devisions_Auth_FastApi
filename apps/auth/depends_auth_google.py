from authlib.integrations.starlette_client import OAuth  # type: ignore
from starlette.config import Config  # type: ignore

from apps.config import settings


class GoggleAuth:
    GOOGLE_CLIENT_ID: str | None = settings.GOOGLE_CLIENT_ID or None
    GOOGLE_CLIENT_SECRET: str | None = settings.GOOGLE_CLIENT_SECRET or None
    if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
        raise BaseException("Missing env variables")

    # Set up OAuth
    config_data: dict = {
        "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
        "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET,
    }
    starlette_config: Config = Config(environ=config_data)
    oauth: OAuth = OAuth(starlette_config)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    SECRET_KEY: str | None = settings.SECRET_KEY or None

    if SECRET_KEY is None:
        raise TypeError("Missing SECRET_KEY")

    FRONTEND_URL: str = "http://127.0.0.1:8000/token"
    FRONTEND_URL_LOGIN: str = "http://127.0.0.1:8000/auth/login"
