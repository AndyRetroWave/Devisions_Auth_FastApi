import asyncio
import json
import pytest
from sqlalchemy import insert
from apps.database import Base, async_session_maker, engine
from apps.config import settings
from apps.user.models import User


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def open_mock_json(model: str):
        with open("apps/tests/mock_users.json", "r") as f:
            return json.load(f)

    user_mock = await open_mock_json("user")

    async with async_session_maker() as session:
        for user in user_mock:
            add_users = insert(User).values(user)
            await session.execute(add_users)
            await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
