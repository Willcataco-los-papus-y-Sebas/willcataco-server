from fastapi import APIRouter, status

from app.core.response_schema import IResponse

from app.modules.water_meters.streets.controllers import StreetControllers
from app.core.database import SessionDep

from app.modules.water_meters.streets.model.schemas import (StreetBase, StreetPatch)

router = APIRouter()


@router.post("/", status_code = status.HTTP_201_CREATED, response_model= IResponse)
async def create_street(session: SessionDep, street_info: StreetBase):
    return await StreetControllers.create_street(session, street_info)

@router.get("/{id}", status_code= status.HTTP_200_OK, response_model= IResponse)
async def read_street(session: SessionDep, id: int):
    return await StreetControllers.read_street(session, id)


@router.patch("/{id}", status_code= status.HTTP_200_OK, response_model= IResponse)
async def patch_information_street(session: SessionDep, id: int, street_info: StreetPatch):
    return await StreetControllers.patch_info_street(session, id, street_info)


@router.delete("/{id}", status_code= status.HTTP_200_OK, response= IResponse)
async def delete_street(session: SessionDep, id: int):
    return await StreetControllers.delete_street(session, id)