from fastapi import HTTPException
from app.core.response_schema import IResponse
from app.core.database import SessionDep
from app.modules.water_meters.water_meazure.services import WaterMeazureService
from app.modules.water_meters.water_meazure.model.schemas import (
    WaterMeterBase, 
    WaterMeterPatch
)

class WaterMeterController:
    @staticmethod
    async def create_meazure(session: SessionDep, meter_info: WaterMeterBase):
        meter = await WaterMeazureService.create_meazure(session, meter_info)
        return IResponse(detail="Water meazure created", status_code=201, data=meter)

    @staticmethod
    async def read_meazure(id: int, session: SessionDep):
        meter = await WaterMeazureService.get_meazure_by_id(session, id)
        if not meter:
            raise HTTPException(status_code=404, detail="Water meazure not found")
        return IResponse(detail="Water meazure found", status_code=200, data=meter)

    @staticmethod
    async def get_all_meazures(session: SessionDep):
        meters = await WaterMeazureService.get_all_meazures(session)
        return IResponse(detail="Water meazures list", status_code=200, data=meters)

    @staticmethod
    async def patch_meazure(id: int, session: SessionDep, meter_info: WaterMeterPatch):
        meter = await WaterMeazureService.get_meazure_by_id(session, id)
        if not meter:
            raise HTTPException(status_code=404, detail="Water meazures not found")
        
        meter_patched = await WaterMeazureService.patch_meazure(session, id, meter_info)
        return IResponse(detail="Water meazure updated", status_code=200, data=meter_patched)
    
    @staticmethod
    async def delete_meazure(id: int, session: SessionDep):
        deleted = await WaterMeazureService.delete_meazure(session, id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Water meazure not found")
            
        return IResponse(detail="Water meazure deleted", status_code=200)