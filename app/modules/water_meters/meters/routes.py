from fastapi import APIRouter, Depends, status

from app.core.database import SessionDep
from app.core.dependencies import RequireRoles
from app.core.enums import UserRole
from app.core.response_schema import IResponse
from app.modules.water_meters.meters.controllers import MeterController
from app.modules.water_meters.meters.model.schemas import MeterBase, MeterPatch

router = APIRouter()


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))],
)
async def delete_meter(id: int, session: SessionDep):
    return await MeterController.delete_meter(id, session)


@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
)
async def patch_meter(id: int, session: SessionDep, meter_info: MeterPatch):
    return await MeterController.patch_meter(id, session, meter_info)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
)
async def read_meter(id: int, session: SessionDep):
    return await MeterController.read_meter(id, session)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IResponse,
)
async def create_meter(session: SessionDep, meter_info: MeterBase):
    return await MeterController.create_meter(session, meter_info)
