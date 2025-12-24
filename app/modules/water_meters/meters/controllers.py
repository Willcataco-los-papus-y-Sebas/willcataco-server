from fastapi import HTTPException

from app.core.database import SessionDep
from app.core.response_schema import IResponse
from app.modules.water_meters.meters.model.schemas import MeterBase
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
    async def update_meter(id: int, session: SessionDep, meter_info: MeterBase):
        meter = await MeterServices.get_meter_by_id(session, id)
        if not meter:
            raise HTTPException(status_code=404, detail="meter not found")
        meter_patched = await MeterServices.update_meter(session, id, meter_info)
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
