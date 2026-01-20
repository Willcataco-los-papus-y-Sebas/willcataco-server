from datetime import datetime
from decimal import Decimal
from pydantic import NonNegativeFloat 

from app.core.email import EmailSession
from app.core.response_schema import IResponse
from app.modules.email.schemas import EmailBase
from app.modules.email.services import EmailService


class EmailController:
    @staticmethod
    async def send_email(email_session: EmailSession, email: EmailBase):
        await EmailService.send_email(email_session, email)
        return IResponse(detail="Email sent successfully", status_code=200)
    
    @staticmethod
    async def send_water_payment_email(
        email_session: EmailSession, 
        email: EmailBase,
        name_member: str,
        last_name_member: str,
        ci_member: str,
        id_payment: int,
        water_reading: Decimal,
        date_created: datetime,
        date_updated: datetime,
        amount: NonNegativeFloat 
    ):
        await EmailService.send_water_payment_email(
            email_session, 
            email,
            name_member,
            last_name_member,
            ci_member,
            id_payment,
            water_reading,
            date_created,
            date_updated,
            amount
        )
        return IResponse(detail="Email sent successfully", status_code=200)
