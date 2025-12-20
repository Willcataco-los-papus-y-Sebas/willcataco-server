from fastapi import HTTPException
from app.core.response_schema import IResponse
from app.core.database import SessionDep
from app.modules.water_meters.water_meters.services import WaterMeterService
from app.modules.water_meters.water_meters.model.schemas import (
    WaterMeterBase, 
    WaterMeterPatch
)

class WaterMeterController:
    @staticmethod
    async def create_meter(session: SessionDep, meter_info: WaterMeterBase):
        meter = await WaterMeterService.create_meter(session, meter_info)
        return IResponse(detail="Water meter created", status_code=201, data=meter)

    @staticmethod
    async def read_meter(id: int, session: SessionDep):
        meter = await WaterMeterService.get_meter_by_id(session, id)
        if not meter:
            raise HTTPException(status_code=404, detail="Water meter not found")
        return IResponse(detail="Water meter found", status_code=200, data=meter)

    @staticmethod
    async def get_all_meters(session: SessionDep):
        meters = await WaterMeterService.get_all_meters(session)
        return IResponse(detail="Water meters list", status_code=200, data=meters)

    @staticmethod
    async def patch_meter(id: int, session: SessionDep, meter_info: WaterMeterPatch):
        meter = await WaterMeterService.get_meter_by_id(session, id)
        if not meter:
            raise HTTPException(status_code=404, detail="Water meter not found")
        
        meter_patched = await WaterMeterService.patch_meter(session, id, meter_info)
        return IResponse(detail="Water meter updated", status_code=200, data=meter_patched)

    @staticmethod
    async def delete_meter(id: int, session: SessionDep):
        meter = await WaterMeterService.get_meter_by_id(session, id)
        if not meter:
            raise HTTPException(status_code=404, detail="Water meter not found")
            
        await WaterMeterService.delete_meter(session, id)
        return IResponse(detail="Water meter deleted", status_code=200)