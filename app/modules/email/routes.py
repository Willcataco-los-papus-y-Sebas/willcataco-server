from fastapi import APIRouter, status

from app.core.dependencies import CurrentUserFlexible
from app.core.email import EmailSession
from app.core.response_schema import IResponse
from app.modules.email.controllers import EmailController
from app.modules.email.schemas import EmailBase, EmailWaterReceiptBase, WaterBillEmailParams

router = APIRouter()



@router.post("/", status_code=status.HTTP_200_OK, response_model=IResponse)
async def send_email(email_session: EmailSession, email: EmailBase):
    return await EmailController.send_email(email_session, email)

@router.post("/water-bill", status_code=status.HTTP_200_OK, response_model=IResponse)
async def send_water_bill(
    email_session: EmailSession, 
    bill_data: WaterBillEmailParams,
    user: CurrentUserFlexible
):
    return await EmailController.send_water_bill_email(
        email_session, 
        bill_data,
        user
    )

@router.post("/water-receipt", status_code=status.HTTP_200_OK, response_model=IResponse)
async def send_water_payment_email(
    email_session: EmailSession, 
    email: EmailBase,
    email_receipt: EmailWaterReceiptBase,
    current_user: CurrentUserFlexible
):
    return await EmailController.send_water_payment_email(
        email_session, 
        email,
        email_receipt,
        current_user
    )