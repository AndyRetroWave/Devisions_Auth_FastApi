
from sqlalchemy import insert, select
from apps.dao.base import BaseDAO
from apps.database import async_session_maker, engine
from apps.user.models import User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_user(
        cls,
        given_names: str,
        family_names: str,
        email: str,
        password: str,
    ):
        async with async_session_maker() as session:

            user = insert(User).values(
                given_name=given_names, family_name=family_names, email=email,
                hashed_password=password)
            # print(user.compile(
            #     engine, compile_kwargs={"loteral_binds": True}))
            await session.execute(user)
            await session.commit()

    @classmethod
    async def get_user_by_email(cls, email: str):
        async with async_session_maker() as session:
            query = select(User).where(User.email == email)
            result = await session.execute(query)
            return result.scalar_one_or_none()
