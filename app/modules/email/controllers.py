from app.core.email import EmailSession
from app.core.response_schema import IResponse
from app.modules.email.schemas import EmailBase
from app.modules.email.services import EmailService


class EmailController:
    @staticmethod
    async def send_email(email_session: EmailSession, email: EmailBase):
        await EmailService.send_email(email_session, email)
        return IResponse(detail="Email sent successfully", status_code=200)
