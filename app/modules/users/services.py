from pydantic import EmailStr
from sqlalchemy import func, select, update

from app.core.database import SessionDep
from app.modules.auth.hashing import Hasher
from app.modules.users.model.models import User
from app.modules.users.model.schemas import (
    UserBase,
    UserPatch,
    UserResponse,
)


class UserService:
    @staticmethod
    async def get_all(session: SessionDep):
        try:
            user = await session.execute(
                select(User).where(User.is_active).order_by(User.id)
            )
            users_orm = user.scalars().all()
            return [UserResponse.model_validate(use) for use in users_orm]
        except Exception:
            raise

    @staticmethod
    async def get_user_by_id(session: SessionDep, id: int):
        try:
            result = await session.execute(
                select(User).where(User.id == id).where(User.is_active)
            )
            user_orm = result.scalars().one_or_none()
            return UserResponse.model_validate(user_orm) if user_orm else None
        except Exception:
            raise

    @staticmethod
    async def get_user_by_email(session: SessionDep, email: EmailStr):
        try:
            result = await session.execute(
                select(User).where(User.email == email).where(User.is_active)
            )
            user_orm = result.scalars().one_or_none()
            return UserResponse.model_validate(user_orm) if user_orm else None
        except Exception:
            raise

    @staticmethod
    async def get_user_by_username(session: SessionDep, username: str):
        try:
            result = await session.execute(
                select(User).where(User.username == username).where(User.is_active)
            )
            user_orm = result.scalars().one_or_none()
            return UserResponse.model_validate(user_orm) if user_orm else None
        except Exception:
            raise

    @staticmethod
    async def delete_user(session: SessionDep, id: int):
        try:
            user = await session.execute(
                select(User).where(User.id == id).where(User.is_active)
            )
            user_orm = user.scalars().one()
            user_orm.is_active = False
            user_orm.deleted_at = func.now()
            await session.commit()
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def patch_information_user(
        session: SessionDep, id: int, user_info: UserPatch
    ):
        try:
            user = await session.execute(select(User).where(User.id == id))
            user_orm = user.scalars().one()
            if user_info.username is not None:
                user_orm.username = user_info.username
            if user_info.email is not None:
                user_orm.email = user_info.email
            if user_info.password is not None:
                user_orm.password = Hasher.get_password_hash(user_info.password)
            if user_info.role is not None:
                user_orm.role = user_info.role
            await session.commit()
            await session.refresh(user_orm)
            return UserResponse.model_validate(user_orm)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def create_user(session: SessionDep, user_info: UserBase):
        try:
            new_user = User(
                username=user_info.username,
                email=user_info.email,
                password=Hasher.get_password_hash(user_info.password),
                role=user_info.role,
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return UserResponse.model_validate(new_user)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def authenticate_user(session: SessionDep, username: str, password: str):
        try:
            user = await session.execute(select(User).where(User.username == username))
            user_orm = user.scalars().one_or_none()
            if not user_orm or not user_orm.is_active:
                return None
            if not Hasher.verify_password(password, user_orm.password):
                return None
            return UserResponse.model_validate(user_orm)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def reset_password(session: SessionDep, id: int, new: str):
        try:
            user = await session.execute(
                update(User)
                .where(User.id == id)
                .values(password=Hasher.get_password_hash(new))
                .returning(User)
            )
            user_orm = user.scalar_one_or_none()
            await session.commit()
            if not user:
                return None
            return UserResponse.model_validate(user_orm)
        except Exception:
            await session.rollback()
            raise
