from fastapi import APIRouter, status

from app.core.dependencies import CurrentUserFlexible
from app.core.email import EmailSession
from app.core.response_schema import IResponse
from app.modules.email.controllers import EmailController
from app.modules.email.schemas import EmailBase, WaterBillEmailParams

router = APIRouter()



@router.post("/", status_code=status.HTTP_200_OK, response_model=IResponse)
async def send_email(email_session: EmailSession, email: EmailBase):
    return await EmailController.send_email(email_session, email)

@router.post("/test-bill", status_code=status.HTTP_200_OK, response_model=IResponse)
async def send_water_bill(
    email_session: EmailSession, 
    bill_data: WaterBillEmailParams,
    user: CurrentUserFlexible
):
    email = EmailBase(recipient=bill_data.recipient, subject=bill_data.subject)
    return await EmailController.send_water_bill_email(
        email_session, 
        email, 
        bill_data.name, 
        bill_data.reading_value, 
        bill_data.date, 
        bill_data.months_owed
    )
