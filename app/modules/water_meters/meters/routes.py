from fastapi import APIRouter, status

from app.core.database import SessionDep
from app.core.response_schema import IResponse
from app.modules.water_meters.meters.controllers import MeterController
from app.modules.water_meters.meters.model.schemas import MeterBase

router = APIRouter()


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
)
async def delete_meter(id: int, session: SessionDep):
    return await MeterController.delete_meter(id, session)


@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
)
async def patch_meter(id: int, session: SessionDep, meter_info: MeterBase):
    return await MeterController.patch_meter(id, session, meter_info)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
)
async def read_meter(id: int, session: SessionDep):
    return await MeterController.read_meter(id, session)
