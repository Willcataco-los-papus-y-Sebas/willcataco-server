from fastapi import APIRouter, status, Depends

from app.core.response_schema import IResponse
from app.core.dependencies import RequireRoles
from app.core.enums import UserRole

from app.modules.water_meters.streets.controllers import StreetControllers
from app.core.database import SessionDep

from app.modules.water_meters.streets.model.schemas import (StreetBase, StreetPatch)

router = APIRouter()


@router.post("/", status_code = status.HTTP_201_CREATED, response_model= IResponse, dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))])
async def create_street(session: SessionDep, street_info: StreetBase):
    return await StreetControllers.create_street(session, street_info)


@router.get("/", status_code= status.HTTP_200_OK, response_model= IResponse, dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))])
async def get_all_streets(session: SessionDep):
    return await StreetControllers.get_all_streets(session)


@router.get("/{id}", status_code= status.HTTP_200_OK, response_model= IResponse, dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))])
async def read_street(session: SessionDep, id: int):
    return await StreetControllers.read_street(session, id)


@router.patch("/{id}", status_code= status.HTTP_200_OK, response_model= IResponse, dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))])
async def patch_information_street(session: SessionDep, id: int, street_info: StreetPatch):
    return await StreetControllers.patch_info_street(session, id, street_info)


@router.delete("/{id}", status_code= status.HTTP_200_OK, response_model= IResponse, dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))])
async def delete_street(session: SessionDep, id: int):
    return await StreetControllers.delete_street(session, id)