from app.core.dependencies import SessionDep
from app.core.response_schema import IResponse
from app.modules.email.schemas import EmailBase
from app.modules.email.services import EmailService


class EmailController:
    @staticmethod
    async def send_email(session: SessionDep, email: EmailBase):
        await EmailService.send_email(session, email)
        return IResponse(detail="Email sent successfully", status_code=200)
