from datetime import date
from fastapi import HTTPException

from app.core.database import SessionDep
from app.core.dependencies import CurrentUserFlexible
from app.core.enums import UserRole
from app.modules.pdf_generator.services import PdfGenService
from app.core.database import SessionDep

class PdfGenController:
    @staticmethod
    async def get_pdf(curr_user_flex: CurrentUserFlexible):
        if curr_user_flex.role is UserRole.MEMBER:
            raise HTTPException(detail="user dont have privileges", status_code=401)
        return await PdfGenService.get_pdf()

    @staticmethod
    async def get_member_report(session: SessionDep, id: int, curr_user_flex: CurrentUserFlexible):
        if curr_user_flex.role not in [UserRole.ADMIN, UserRole.STAFF]:
            raise HTTPException(
                status_code=403, 
                detail="Insufficient privileges"
            )   
        return await PdfGenService.generate_member_report(session, id)
    
    @staticmethod
    async def get_new_members_report(
        session: SessionDep,
        curr_user_flex: CurrentUserFlexible,
        start_date: date,
        end_date: date,
    ):
        if curr_user_flex.role is UserRole.MEMBER:
            raise HTTPException(detail="user dont have privileges", status_code=401)

        if end_date < start_date:
            raise HTTPException(status_code=400, detail="invalid date range")

        return await PdfGenService.get_new_members_report(session, start_date, end_date)

    @staticmethod
    async def get_extra_payments_catalog_report(
        session: SessionDep,
        curr_user_flex: CurrentUserFlexible,
        start_date: date,
        end_date: date,
    ):
        if curr_user_flex.role is UserRole.MEMBER:
            raise HTTPException(detail="user dont have privileges", status_code=401)

        if end_date < start_date:
            raise HTTPException(status_code=400, detail="invalid date range")

        return await PdfGenService.get_extra_payments_catalog_report(session, start_date, end_date)
