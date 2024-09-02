from datetime import datetime, timedelta
from pathlib import Path
import aiofiles
import jwt
from apps.config import settings


async def read_key(path: Path) -> str:
    async with aiofiles.open(path, mode='r') as f:
        return await f.read()


async def encode_jwt(
    payload: dict,
    algorithm: str = settings.AUTH_JWT.algorithm
):
    to_encode = payload.copy()
    expire = datetime.now() + timedelta(minutes=settings.API_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire
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


def validate_user():
    pass
