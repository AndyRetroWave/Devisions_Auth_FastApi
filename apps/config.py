from pathlib import Path
from typing import Literal

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "apps" / "certs" / "private_key.pem"
    public_key_path: Path = BASE_DIR / "apps" / "certs" / "public_key.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 60 * 24 * 30


class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"

    DB_USER: str
    DB_PASS: SecretStr
    DB_PORT: int
    DB_HOST: str
    DB_NAME: str

    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_PORT: int
    TEST_DB_HOST: str
    TEST_DB_NAME: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    SECRET_KEY: str

    API_SECRET_KEY: str
    API_ALGORITHM: str

    AUTH_JWT: AuthJWT = AuthJWT()

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://\
{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def TEST_DB_URL(self):
        return f"postgresql+asyncpg://\
{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"


settings = Setting()
