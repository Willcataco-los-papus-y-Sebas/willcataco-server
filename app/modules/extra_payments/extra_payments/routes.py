from fastapi import APIRouter, status, Depends, Query

from app.core.database import SessionDep
from app.core.dependencies import RequireRoles
from app.core.enums import UserRole
from app.core.response_schema import IResponse

from app.modules.extra_payments.extra_payments.controllers import (
    ExtraPaymentController
)
from app.modules.extra_payments.extra_payments.schemas import (
    ExtraPaymentCreate,
    ExtraPaymentUpdate,
)

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))]
)
async def read_extra_payments(
    session: SessionDep,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return await ExtraPaymentController.read_all(session, limit, offset)


@router.get(
    "/{payment_id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))]
)
async def read_extra_payment(payment_id: int, session: SessionDep):
    return await ExtraPaymentController.read_by_id(session, payment_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))]
)
async def create_extra_payment(
    session: SessionDep,
    data: ExtraPaymentCreate
):
    return await ExtraPaymentController.create(session, data)


@router.patch(
    "/{payment_id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))]
)
async def update_extra_payment(
    payment_id: int,
    session: SessionDep,
    data: ExtraPaymentUpdate
):
    return await ExtraPaymentController.update(
        session,
        payment_id,
        data
    )


@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))]
)
async def delete_extra_payment(payment_id: int, session: SessionDep):
    return await ExtraPaymentController.delete(session, payment_id)
