from sqlalchemy import select, func
from app.core.database import SessionDep
from app.modules.water_meters.water_measure.model.models import WaterMeter
from app.modules.water_meters.water_measure.model.schemas import (
    WaterMeterBase,
    WaterMeterPatch,
    WaterMeterResponse,
)

class WaterMeasureService:
    @staticmethod
    async def get_measure_by_id(session: SessionDep, id: int):
        try:
            stmt = select(WaterMeter).where(
                WaterMeter.id == id, 
                WaterMeter.deleted_at.is_(None)
            )
            result = await session.execute(stmt)
            meter_orm = result.scalars().one_or_none()
            if not meter_orm:
                return None
                
            return WaterMeterResponse.model_validate(meter_orm)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_all_measures(session: SessionDep):
        try:
            stmt = select(WaterMeter).where(WaterMeter.deleted_at.is_(None))
            result = await session.execute(stmt)
            meters_orm = result.scalars().all()
            return [WaterMeterResponse.model_validate(m) for m in meters_orm]
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def create_measure(session: SessionDep, meter_info: WaterMeterBase):
        try:
            new_meter = WaterMeter(
                action_id=meter_info.action_id,
                water_reading=meter_info.water_reading
            )
            session.add(new_meter)
            await session.commit()
            await session.refresh(new_meter)
            return WaterMeterResponse.model_validate(new_meter)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def patch_measure(session: SessionDep, id: int, meter_info: WaterMeterPatch):
        try:
            stmt = select(WaterMeter).where(
                WaterMeter.id == id, 
                WaterMeter.deleted_at.is_(None)
            )
            result = await session.execute(stmt)
            meter_orm = result.scalars().one_or_none()
            if not meter_orm:
                return None

            if meter_info.action_id is not None:
                meter_orm.action_id = meter_info.action_id
            if meter_info.water_reading is not None:
                meter_orm.water_reading = meter_info.water_reading
            
            await session.commit()
            await session.refresh(meter_orm)
            return WaterMeterResponse.model_validate(meter_orm)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def delete_measure(session: SessionDep, id: int):
        try:
            stmt = select(WaterMeter).where(
                WaterMeter.id == id, 
                WaterMeter.deleted_at.is_(None)
            )
            result = await session.execute(stmt)
            meter_orm = result.scalars().one_or_none()
            if not meter_orm:
                return None 
            
            meter_orm.deleted_at = func.now()
            
            await session.commit()
            return True 
        except Exception:
            await session.rollback()
            raise