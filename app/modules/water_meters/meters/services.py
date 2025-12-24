from sqlalchemy import Update, func, select

from app.core.database import SessionDep
from app.modules.water_meters.meters.model.models import Meter
from app.modules.water_meters.meters.model.schemas import (
    MeterBase,
    MeterResponse,
)


class MeterServices:
    @staticmethod
    async def get_meter_by_id(session: SessionDep, id: int):
        try:
            result = await session.execute(select(Meter).where(Meter.id == id))
            meter_orm = result.scalars().one_or_none()
            return MeterResponse.model_validate(meter_orm) if meter_orm else None
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def delete_meter(id: int, session: SessionDep):
        try:
            meter = await session.execute(select(Meter).where(Meter.id == id))
            meter_orm = meter.scalars().one()
            meter_orm.deleted_at = func.now()
            await session.commit()
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def update_meter(session: SessionDep, id: int, meter_info: MeterBase):
        try:
            meter = await session.execute(
                Update(Meter)
                .where(Meter.id == id)
                .values(**meter_info.model_dump())
                .returning(Meter)
            )
            meter_orm = meter.scalar_one_or_none()
            await session.commit()
            if not meter_orm:
                return None
            return MeterResponse.model_validate(meter_orm)
        except Exception:
            await session.rollback()
            raise
