from fastapi import APIRouter, status
from datetime import datetime
from decimal import Decimal
from pydantic import NonNegativeFloat 

from app.core.email import EmailSession
from app.core.response_schema import IResponse
from app.modules.email.controllers import EmailController
from app.modules.email.schemas import EmailBase

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=IResponse)
async def send_email(email_session: EmailSession, email: EmailBase):
    return await EmailController.send_email(email_session, email)

@router.post("/", status_code=status.HTTP_200_OK, response_model=IResponse)
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
    return await EmailController.send_water_payment_email(
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
