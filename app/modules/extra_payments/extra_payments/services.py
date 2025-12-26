from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.core.database import SessionDep
from app.modules.extra_payments.extra_payments.model.models import ExtraPayment
from app.modules.extra_payments.extra_payments.schemas import (
    ExtraPaymentCreate,
    ExtraPaymentUpdate,
    ExtraPaymentResponse,
)


class ExtraPaymentService:

    @staticmethod
    async def get_all(session: SessionDep):
        try:
            result = await session.execute(
                select(ExtraPayment)
                .where(ExtraPayment.deleted_at.is_(None))
                .order_by(ExtraPayment.created_at.desc())
            )
            payments = result.scalars().all()
            return [ExtraPaymentResponse.model_validate(p) for p in payments]
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_by_id(session: SessionDep, payment_id: int):
        try:
            result = await session.execute(
                select(ExtraPayment).where(
                    ExtraPayment.id == payment_id,
                    ExtraPayment.deleted_at.is_(None),
                )
            )
            payment = result.scalars().one_or_none()
            return (
                ExtraPaymentResponse.model_validate(payment)
                if payment
                else None
            )
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def create(session: SessionDep, data: ExtraPaymentCreate):
        try:
            new_payment = ExtraPayment(**data.model_dump())
            session.add(new_payment)
            await session.commit()
            await session.refresh(new_payment)
            return ExtraPaymentResponse.model_validate(new_payment)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def update(
        session: SessionDep,
        payment_id: int,
        data: ExtraPaymentUpdate,
    ):
        try:
            await session.execute(
                update(ExtraPayment)
                .where(
                    ExtraPayment.id == payment_id,
                    ExtraPayment.deleted_at.is_(None),
                )
                .values(**data.model_dump(exclude_unset=True))
            )
            await session.commit()
            return await ExtraPaymentService.get_by_id(session, payment_id)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def delete_logical(session: SessionDep, payment_id: int):
        try:
            await session.execute(
                update(ExtraPayment)
                .where(
                    ExtraPayment.id == payment_id,
                    ExtraPayment.deleted_at.is_(None),
                )
                .values(deleted_at=datetime.utcnow())
            )
            await session.commit()
        except Exception:
            await session.rollback()
            raise
