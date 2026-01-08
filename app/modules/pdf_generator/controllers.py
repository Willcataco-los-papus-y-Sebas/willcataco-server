from fastapi import HTTPException

from app.core.dependencies import CurrentUserFlexible
from app.core.enums import UserRole
from app.modules.pdf_generator.services import PdfGenService


class PdfGenController:
    @staticmethod
    async def get_pdf(curr_user_flex: CurrentUserFlexible):
        if curr_user_flex.role is UserRole.MEMBER:
            raise HTTPException(detail="user dont have privileges", status_code=401)
        return await PdfGenService.get_pdf()
