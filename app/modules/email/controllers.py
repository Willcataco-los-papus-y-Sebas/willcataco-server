from fastapi import HTTPException

from app.core.dependencies import CurrentUserFlexible
from app.core.email import EmailSession
from app.core.enums import UserRole
from app.core.response_schema import IResponse
from app.modules.email.schemas import EmailBase, WaterBillEmailParams
from app.modules.email.services import EmailService


class EmailController:
    @staticmethod
    async def send_email(email_session: EmailSession, email: EmailBase):
        await EmailService.send_email(email_session, email)
        return IResponse(detail="Email sent successfully", status_code=200)

    @staticmethod
    async def send_water_bill_email(
        email_session: EmailSession, 
        bill_data: WaterBillEmailParams,
        user: CurrentUserFlexible
    ):
        if user.role not in [UserRole.ADMIN, UserRole.STAFF]:
            raise HTTPException(status_code=403, detail="Not enough permissions")
            
        await EmailService.send_water_bill_email(
            email_session, bill_data
        )
        return IResponse(detail="Water Bill Email sent successfully", status_code=200)
