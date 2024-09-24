from fastapi import HTTPException, status
from sqlalchemy import insert, select

from apps.database import async_session_maker
from apps.user.models import User


class BaseDAO:
    model = User()

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)  # type: ignore
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_scalar(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()


class UserDAO(BaseDAO):
    model = User()  # type: ignore

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
                    given_name=given_names,
                    family_name=family_names,
                    email=email,
                    hashed_password=password,
                )  # type: ignore
                # print(user.compile(
                #     engine, compile_kwargs={"loteral_binds": True}))
                await session.execute(user)
                await session.commit()
                return user
        except:  # noqa: E722
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    @classmethod
    async def get_user_by_email(cls, email: str):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.email == email)  # type: ignore
            result = await session.execute(query)
            return result.scalar_one_or_none()
