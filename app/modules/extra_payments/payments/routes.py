from fastapi import APIRouter, Depends, status, Query

from app.core.database import SessionDep
from app.core.dependencies import RequireRoles
from app.core.enums import UserRole
from app.core.response_schema import IResponse
from app.modules.extra_payments.payments.controllers import PaymentController
from app.modules.extra_payments.payments.model.schemas import PaymentCreate, PaymentPatch

router = APIRouter()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))],
)
async def create_payment(session: SessionDep, payment_info: PaymentCreate):
    return await PaymentController.create_payment(session, payment_info)

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))],
)
async def read_payment(id: int, session: SessionDep):
    return await PaymentController.read_payment(id, session)

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))],
)
async def read_all_payments(
    session: SessionDep, 
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, gt=0)
):
    return await PaymentController.read_all_payments(session, skip, limit)

@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))],
)
async def update_payment(id: int, session: SessionDep, payment_info: PaymentPatch):
    return await PaymentController.update_payment(id, session, payment_info)

@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))],
)
async def delete_payment(id: int, session: SessionDep):
    return await PaymentController.delete_payment(id, session)
