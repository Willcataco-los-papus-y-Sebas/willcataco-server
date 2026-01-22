from app.core.email import EmailSession
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
        bill_data: WaterBillEmailParams
    ):
        await EmailService.send_water_bill_email(
            email_session, bill_data
        )
        return IResponse(detail="Water Bill Email sent successfully", status_code=200)
