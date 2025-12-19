import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.mapping_database  # noqa: F401
from app.core.enums import UserRole
from app.modules.users.model.models import User

logger = logging.getLogger(__name__)

async def seed_users(session: AsyncSession):
    users_data = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "password": "$argon2id$v=19$m=65536,t=3,p=4$u5HqWzVrDEhq3afghK8B9A$7JSi17WVwoCvaqtki4sKH/vAGElFJKElCya2Aa0v0LY",  # TODO: Hash this password
            "role": UserRole.ADMIN,
            "is_active": True
        },
        {
            "username": "staff",
            "email": "staff@example.com",
            "password": "$argon2id$v=19$m=65536,t=3,p=4$u5HqWzVrDEhq3afghK8B9A$7JSi17WVwoCvaqtki4sKH/vAGElFJKElCya2Aa0v0LY",  # TODO: Hash this password
            "role": UserRole.STAFF,
            "is_active": True
        },
        {
            "username": "member",
            "email": "member@example.com",
            "password": "$argon2id$v=19$m=65536,t=3,p=4$u5HqWzVrDEhq3afghK8B9A$7JSi17WVwoCvaqtki4sKH/vAGElFJKElCya2Aa0v0LY",  # TODO: Hash this password
            "role": UserRole.MEMBER,
            "is_active": True
        }
    ]

    for user_data in users_data:
        stmt = select(User).where(User.email == user_data["email"])
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            new_user = User(**user_data)
            session.add(new_user)
            logger.info(f"Creating user: {user_data['username']} with role {user_data['role'].value}")
        else:
            logger.info(f"User {user_data['username']} already exists.")
