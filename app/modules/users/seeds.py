import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.model.models import User
from app.modules.members.model.models import Member 
from app.modules.extra_payments.payments.model.models import Payment
from app.modules.extra_payments.extra_payments.model.models import ExtraPayment
from app.modules.water_meters.actions.model.models import Action
from app.modules.water_meters.water_payments.model.models import WaterPayment
from app.modules.water_meters.streets.model.models import Street
from app.modules.water_meters.action_payments.model.models import ActionPayment
from app.modules.water_meters.water_meters.model.models import WaterMeter
from app.modules.water_meters.meters.model.models import Meter
from app.core.enums import UserRole

logger = logging.getLogger(__name__)

async def seed_users(session: AsyncSession):
    users_data = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "password": "password123",  # TODO: Hash this password
            "role": UserRole.ADMIN,
            "is_active": True
        },
        {
            "username": "staff",
            "email": "staff@example.com",
            "password": "password123",  # TODO: Hash this password
            "role": UserRole.STAFF,
            "is_active": True
        },
        {
            "username": "member",
            "email": "member@example.com",
            "password": "password123",  # TODO: Hash this password
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
