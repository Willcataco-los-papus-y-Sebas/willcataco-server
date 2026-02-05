from datetime import date, datetime, time, timedelta
from sqlalchemy import select, update, func
from app.core.database import SessionDep
from app.modules.extra_payments.extra_payments.model.models import ExtraPayment
from app.modules.extra_payments.extra_payments.schemas import (
    ExtraPaymentCreate,
    ExtraPaymentUpdate,
    ExtraPaymentResponse,
)


class ExtraPaymentService:

    @staticmethod
    async def get_all(
        session: SessionDep,
        limit: int,
        offset: int
    ):
        try:
            result = await session.execute(
                select(ExtraPayment)
                .where(ExtraPayment.deleted_at.is_(None))
                .order_by(ExtraPayment.created_at.desc())
                .limit(limit)
                .offset(offset)
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
                .values(deleted_at=func.now())
            )
            await session.commit()
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_between_dates(session: SessionDep, start_date: datetime, end_date: datetime, only_active: bool):
        try:
            start_dt = datetime.combine(start_date, time.min)#CAMBIAR
            end_exclusive = datetime.combine(end_date + timedelta(days=1), time.min)

            query = (
                select(ExtraPayment)
                .where(ExtraPayment.deleted_at.is_(None))
                .where(ExtraPayment.created_at >= start_dt)
                .where(ExtraPayment.created_at < end_exclusive)
                .order_by(ExtraPayment.created_at.desc(), ExtraPayment.name)
            )

            if only_active:
                query = query.where(ExtraPayment.is_active)

            result = await session.execute(query)
            extras = result.scalars().all()
            return [ExtraPaymentResponse.model_validate(e) for e in extras]
        except Exception:
            await session.rollback()
            raise