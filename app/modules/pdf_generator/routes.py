from datetime import date
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import StreamingResponse

from app.core.database import SessionDep

from app.core.dependencies import CurrentUserFlexible, RequireRoles
from app.core.enums import UserRole
from app.modules.pdf_generator.controllers import PdfGenController

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    dependencies=[Depends(RequireRoles(UserRole.STAFF, UserRole.ADMIN))],
)
async def get_pdf(curr_user_flex: CurrentUserFlexible):
    return await PdfGenController.get_pdf(curr_user_flex)

@router.get(
    "/member/{id}",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    dependencies=[Depends(RequireRoles(UserRole.STAFF, UserRole.ADMIN))],
)
async def get_member_report(
    id: int, 
    session: SessionDep, 
    curr_user_flex: CurrentUserFlexible
):
    return await PdfGenController.get_member_report(session, id, curr_user_flex)

@router.get(
    "/new-members",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    dependencies=[Depends(RequireRoles(UserRole.STAFF, UserRole.ADMIN))],
)
async def get_new_members_report(
    session: SessionDep,
    curr_user_flex: CurrentUserFlexible,
    start_date: date = Query(...),
    end_date: date = Query(...),
):
    return await PdfGenController.get_new_members_report(
        session, curr_user_flex, start_date, end_date
    )

@router.get(
    "/members-water-payments",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    dependencies=[Depends(RequireRoles(UserRole.STAFF, UserRole.ADMIN))]
)
async def get_members_water_payments_report(
    session: SessionDep,
    curr_user_flex: CurrentUserFlexible,
    start_date: date = Query(...),
    end_date: date = Query(...),
):
    return await PdfGenController.get_members_water_payments_report(
        session, start_date, end_date, curr_user_flex
    )
@router.get("/receipt-extra-payment",
            status_code=status.HTTP_200_OK,
            response_class=StreamingResponse,
            dependencies=[Depends(RequireRoles(UserRole.STAFF, UserRole.ADMIN))],
)
async def get_receipt_extra_payment(
    session: SessionDep,
    curr_user_flex: CurrentUserFlexible,
    payment_id : int = Query(...)
):
    return await PdfGenController.get_receipt_extra_payment(
        session, curr_user_flex, payment_id
    )
