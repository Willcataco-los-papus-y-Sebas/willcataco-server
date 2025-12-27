from fastapi import APIRouter, status, Depends 
from app.core.response_schema import IResponse
from app.core.database import SessionDep
from app.modules.water_meters.water_measure.controllers import WaterMeterController
from app.modules.water_meters.water_measure.model.schemas import (
    WaterMeterBase,
    WaterMeterPatch
)
from app.core.dependencies import RequireRoles
from app.core.enums import UserRole

router = APIRouter()

@router.post(
        "/", 
        status_code=status.HTTP_201_CREATED, 
        response_model=IResponse,
        dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))]
)
async def create_water_measure(session: SessionDep, meter_info: WaterMeterBase):
    return await WaterMeterController.create_measure(session, meter_info)

@router.get(
        "/", 
        status_code=status.HTTP_200_OK, 
        response_model=IResponse
)
async def list_water_measure(session: SessionDep):
    return await WaterMeterController.get_all_measures(session)

@router.get(
        "/{id}", 
        status_code=status.HTTP_200_OK, 
        response_model=IResponse
)
async def read_water_measure(id: int, session: SessionDep):
    return await WaterMeterController.read_measure(id, session)

@router.patch(
    "/{id}", 
    status_code=status.HTTP_200_OK, 
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))] 
)
async def patch_water_measure(id: int, session: SessionDep, meter_info: WaterMeterPatch):
    return await WaterMeterController.patch_measure(id, session, meter_info)

@router.delete(
    "/{id}", 
    status_code=status.HTTP_200_OK, 
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))]
)
async def delete_water_measure(id: int, session: SessionDep):
    return await WaterMeterController.delete_measure(id, session)