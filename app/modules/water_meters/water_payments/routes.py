from fastapi import APIRouter, Depends, status

from app.core.dependencies import RequireRoles
from app.core.database import SessionDep
from app.core.enums import UserRole, PaymentStatus
from app.modules.water_meters.water_payments.controllers import WaterPaymentController
from app.core.response_schema import IResponse
from app.modules.water_meters.water_payments.model.schemas import WaterPaymentBase, WaterPaymentFilter

router = APIRouter()

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
)
async def list_water_payments(
    session: SessionDep,
    filters: WaterPaymentFilter = Depends(),
):
    return await WaterPaymentController.list_water_payments(
        session, filters
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IResponse, 
)
async def create_water_payment(
    session: SessionDep, payment_info: WaterPaymentBase
):
    return await WaterPaymentController.create_water_payment(session, payment_info)

@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
)
async def change_status(
    id: int, session: SessionDep
):
    return await WaterPaymentController.change_status(id, session)

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
)
async def read_water_payment(id: int, session: SessionDep):
    return await WaterPaymentController.read_water_payment(id, session)

@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))],
)
async def delete_water_payment(id: int, session: SessionDep):
    return await WaterPaymentController.delete_water_payment(id, session)
