from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from app.core.database import SessionDep
from app.modules.extra_payments.payments.model.models import Payment
from app.modules.extra_payments.payments.model.schemas import (
    PaymentCreate,
    PaymentPatch,
    PaymentResponse,
)

class PaymentService:
    @staticmethod
    async def get_payment_by_id(session: SessionDep, id: int):
        try:
            result = await session.execute(select(Payment).where(Payment.id == id))
            payment_orm = result.scalars().one_or_none()
            return PaymentResponse.model_validate(payment_orm) if payment_orm else None
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_all_payments(session: SessionDep, skip: int, limit: int):
        try:
            result = await session.execute(
                select(Payment).where(Payment.deleted_at.is_(None)).offset(skip).limit(limit)
            )
            payments_orm = result.scalars().all()
            return [PaymentResponse.model_validate(payment) for payment in payments_orm]
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def create_payment(session: SessionDep, payment_info: PaymentCreate):
        try:
            new_payment = Payment(**payment_info.model_dump())
            session.add(new_payment)
            await session.commit()
            await session.refresh(new_payment)
            return PaymentResponse.model_validate(new_payment)
        except IntegrityError:
            await session.rollback()
            raise ValueError("Member or ExtraPayment ID not found")
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def update_payment(session: SessionDep, id: int, payment_info: PaymentPatch):
        try:
            result = await session.execute(select(Payment).where(Payment.id == id))
            payment_orm = result.scalars().one()
            
            update_data = payment_info.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(payment_orm, key, value)
                
            await session.commit()
            await session.refresh(payment_orm)
            return PaymentResponse.model_validate(payment_orm)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def delete_payment(session: SessionDep, id: int):
        try:
            result = await session.execute(select(Payment).where(Payment.id == id))
            payment_orm = result.scalars().one()
            payment_orm.deleted_at = func.now()
            await session.commit()
        except Exception:
            await session.rollback()
            raise
