from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from app.core.dependencies import CurrentUserFlexible, RequireRoles
from app.core.enums import UserRole
from app.modules.pdf_generator.controllers import PdfGenController
from app.core.database import SessionDep

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