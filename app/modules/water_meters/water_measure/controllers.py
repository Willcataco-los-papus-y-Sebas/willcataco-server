from fastapi import HTTPException
from app.core.response_schema import IResponse
from app.core.database import SessionDep
from app.modules.water_meters.water_measure.services import WaterMeasureService
from app.modules.water_meters.water_measure.model.schemas import (
    WaterMeterBase, 
    WaterMeterPatch
)

class WaterMeterController:
    @staticmethod
    async def create_measure(session: SessionDep, meter_info: WaterMeterBase):
        meter = await WaterMeasureService.create_measure(session, meter_info)
        return IResponse(detail="Water measure created", status_code=201, data=meter)

    @staticmethod
    async def read_measure(id: int, session: SessionDep):
        meter = await WaterMeasureService.get_measure_by_id(session, id)
        if not meter:
            raise HTTPException(status_code=404, detail="Water measure not found")
        return IResponse(detail="Water measure found", status_code=200, data=meter)

    @staticmethod
    async def get_all_measures(session: SessionDep):
        meters = await WaterMeasureService.get_all_measures(session)
        return IResponse(detail="Water measures list", status_code=200, data=meters)

    @staticmethod
    async def patch_measure(id: int, session: SessionDep, meter_info: WaterMeterPatch):
        meter = await WaterMeasureService.get_measure_by_id(session, id)
        if not meter:
            raise HTTPException(status_code=404, detail="Water measures not found")
        
        meter_patched = await WaterMeasureService.patch_measure(session, id, meter_info)
        return IResponse(detail="Water measure updated", status_code=200, data=meter_patched)
    
    @staticmethod
    async def delete_measure(id: int, session: SessionDep):
        deleted = await WaterMeasureService.delete_measure(session, id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Water measure not found")
            
        return IResponse(detail="Water measure deleted", status_code=200)