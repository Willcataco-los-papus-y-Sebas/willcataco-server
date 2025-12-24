from pydantic import NonNegativeFloat
from sqlalchemy import func, select, update

from app.core.database import SessionDep
from app.modules.water_meters.meters.model.models import Meter
from app.modules.water_meters.meters.model.schemas import (
    MeterBase,
    MeterPatch,
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
    async def patch_meter(
        session: SessionDep,
        id: int,
        meter_info: MeterPatch,
        past_read: NonNegativeFloat,
    ):
        try:
            meter_info_update = meter_info.model_dump()
            meter_info_update["past_water_reading"] = past_read
            meter = await session.execute(
                update(Meter)
                .where(Meter.id == id)
                .values(**meter_info_update)
                .returning(Meter)
            )
            meter_orm = meter.scalar_one_or_none()
            if not meter_orm:
                return None
            await session.commit()
            return MeterResponse.model_validate(meter_orm)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def create_meter(session: SessionDep, meter_info: MeterBase):
        pass
