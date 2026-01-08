from fastapi import APIRouter, Depends, status

from app.core.dependencies import CurrentUserFlexible, RequireRoles
from app.core.enums import UserRole
from app.modules.pdf_generator.controllers import PdfGenController

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=Depends[RequireRoles(UserRole.STAFF, UserRole.ADMIN)],
)
async def get_pdf(curr_user_flex: CurrentUserFlexible):
    return await PdfGenController.get_pdf(curr_user_flex)
