from app.core.response_schema import IResponse
from fastapi import HTTPException

from app.modules.water_meters.streets.services import StreetServices

from app.modules.water_meters.streets.model.schemas import StreetBase, StreetPatch, StreetResponse
from app.core.database import SessionDep


class StreetControllers():

    @staticmethod
    async def create_street(session: SessionDep, street_info: StreetBase):
        street_name = await StreetServices.get_street_by_name(session, street_info.name)
        if street_name:
            raise HTTPException(status_code=400, detail="Street already exists")
        street = await StreetServices.create_street(session, street_info)
        response = IResponse(detail="Street created", status_code=201, data=street)
        return response
    

    @staticmethod
    async def patch_info_street(session: SessionDep, id:int, street_info: StreetPatch):
        street = await StreetServices.get_street_by_id(session, id)
        if not street:
            raise HTTPException(status_code=404, detail="Street not found")
        street_patched = await StreetServices.patch_info_street(session, id, street_info)
        response = IResponse(detail="Street patched", status_code=200, data=street_patched)
        return response
    

    @staticmethod
    async def delete_street(session: SessionDep, id: int):
        street = await StreetServices.get_street_by_id(session, id)
        if not street:
            raise HTTPException(status_code=404, detail="Street not found")
        await StreetServices.delete_street(session, id)
        response = IResponse(detail="Street deleted", status_code=200)
        return response
    

    @staticmethod
    async def read_street(session: SessionDep, id: int):
        street = await StreetServices.get_street_by_id(session, id)
        if not street:
            raise HTTPException(status_code=404, detail="Street not found")
        response = IResponse(detail="Street found", status_code=200, data=street)
        return response
    
    

