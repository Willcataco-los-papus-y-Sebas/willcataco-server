from fastapi import HTTPException

from app.core.dependencies import CurrentUserFlexible
from app.core.email import EmailSession
from app.core.enums import UserRole
from app.core.response_schema import IResponse
from app.modules.email.schemas import EmailBase, ExtraPaymentEmailParams
from app.modules.email.services import EmailService


class EmailController:
    @staticmethod
    async def send_email(email_session: EmailSession, email: EmailBase):
        await EmailService.send_email(email_session, email)
        return IResponse(detail="Email sent successfully", status_code=200)

    @staticmethod
    async def send_extra_payment_email(
        email_session: EmailSession,
        payment_data: ExtraPaymentEmailParams,
        user: CurrentUserFlexible,
    ):
        if user.role not in [UserRole.ADMIN, UserRole.STAFF]:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        await EmailService.send_extra_payment_email(email_session, payment_data)
        return IResponse(detail="Email sent successfully", status_code=200)
