from fastapi import HTTPException

from app.core.database import SessionDep
from app.core.response_schema import IResponse
from app.modules.water_meters.meters.model.schemas import MeterBase, MeterPatch
from app.modules.water_meters.meters.services import MeterServices


class MeterController:
    @staticmethod
    async def delete_meter(id: int, session: SessionDep):
        meter = await MeterServices.get_meter_by_id(session, id)
        if not meter:
            raise HTTPException(status_code=404, detail="meter not found")
        await MeterServices.delete_meter(session, id)
        response = IResponse(detail="meter deleted", status_code=200)
        return response

    @staticmethod
    async def patch_meter(id: int, session: SessionDep, meter_info: MeterPatch):
        meter = await MeterServices.get_meter_by_id(session, id)
        if not meter:
            raise HTTPException(status_code=404, detail="meter not found")
        meter_patched = await MeterServices.patch_meter(
            session, id, meter_info, meter.water_reading
        )
        if not meter_patched:
            raise HTTPException(status_code=404, detail="meter not patched")
        response = IResponse(
            detail="meter patched", status_code=200, data=meter_patched
        )
        return response

    @staticmethod
    async def read_meter(id: int, session: SessionDep):
        meter = await MeterServices.get_meter_by_id(session, id)
        if not meter:
            raise HTTPException(status_code=404, detail="meter not found")
        response = IResponse(detail="meter found", status_code=200, data=meter)
        return response

    @staticmethod
    async def create_meter(session: SessionDep, meter_info: MeterBase):
        meter = await MeterServices.create_meter(session , id)
        response = IResponse(detail="meter created", status_code=201, data=meter)
        return response
