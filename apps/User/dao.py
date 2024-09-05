from sqlalchemy import insert, select

from apps.dao.base import BaseDAO
from apps.database import async_session_maker
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
        try:
            async with async_session_maker() as session:
                user = insert(cls.model).values(
                    # id=id_primary_key_result,
                    given_name=given_names,
                    family_name=family_names,
                    email=email,
                    hashed_password=password,
                )
                # print(user.compile(
                #     engine, compile_kwargs={"loteral_binds": True}))
                await session.execute(user)
                await session.commit()
                return user
        except:  # noqa: E722
            return None

    @classmethod
    async def get_user_by_email(cls, email: str):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.email == email)
            result = await session.execute(query)
            return result.scalar_one_or_none()
