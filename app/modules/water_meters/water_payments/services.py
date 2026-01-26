from sqlalchemy import func, select

from app.core.enums import PaymentStatus
from app.core.database import SessionDep
from app.modules.water_meters.water_payments.model.models import WaterPayment
from app.modules.members.model.models import Member
from app.modules.water_meters.meters.model.models import Meter 
from app.modules.water_meters.water_payments.model.schemas import (
    WaterPaymentBase,
    WaterPaymentResponse,
    WaterPaymentFilter,
)


class WaterPaymentService:
    @staticmethod
    async def get_all_water_payments(
        session: SessionDep,
        filters: WaterPaymentFilter,
    ):
        try:
            stmt = select(WaterPayment).where(WaterPayment.deleted_at.is_(None))

            if filters.member_id:
                stmt = stmt.where(WaterPayment.member_id == filters.member_id)

            if filters.status:
                stmt = stmt.where(WaterPayment.status == filters.status)

            if filters.start_date:
                stmt = stmt.where(WaterPayment.created_at >= filters.start_date)

            if filters.end_date:
                stmt = stmt.where(WaterPayment.created_at <= filters.end_date)

            stmt = stmt.limit(filters.limit).offset(filters.offset).order_by(WaterPayment.created_at.desc())

            result = await session.execute(stmt)
            payments_orm = result.scalars().all()
            return [WaterPaymentResponse.model_validate(p) for p in payments_orm]
        except Exception:
            raise

    @staticmethod
    async def get_water_payment_by_id(session: SessionDep, id: int):
        try:
            result = await session.execute(
                select(WaterPayment).where(WaterPayment.id == id)
            )
            payment_orm = result.scalars().one_or_none()
            if not payment_orm:
                return None
            return WaterPaymentResponse.model_validate(payment_orm)
        except Exception:
            raise

    @staticmethod
    async def create_water_payment(session: SessionDep, payment_info: WaterPaymentBase):
        try:
            
            result_member = await session.execute(
                select(Member).where(Member.id == payment_info.member_id)
            )
            member_orm = result_member.scalars().one_or_none()
            if not member_orm:
                return None

            
            result_meter = await session.execute(
                select(Meter).where(Meter.id == payment_info.meter_id)
            )
            meter_orm = result_meter.scalars().one_or_none()
            if not meter_orm:
                return None

            new_payment = WaterPayment(
                member_id=payment_info.member_id,
                meter_id=payment_info.meter_id,
                amount=0.50,
            )
            session.add(new_payment)
            await session.commit()
            await session.refresh(new_payment)
            return WaterPaymentResponse.model_validate(new_payment)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def change_status(session: SessionDep, id: int):
        try:
            result = await session.execute(
                select(WaterPayment).where(WaterPayment.id == id)
            )
            payment_orm = result.scalar_one_or_none()
            if not payment_orm:
                return None
            payment_orm.status = PaymentStatus.PAID
            await session.commit()
            await session.refresh(payment_orm)
            return WaterPaymentResponse.model_validate(payment_orm)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def delete_water_payment(session: SessionDep, id: int):
        try:
            result = await session.execute(
                select(WaterPayment).where(WaterPayment.id == id)
            )
            payment_orm = result.scalar_one_or_none()
            if not payment_orm:
                return None
            payment_orm.deleted_at = func.now()
            await session.commit()
        except Exception:
            await session.rollback()
            raise