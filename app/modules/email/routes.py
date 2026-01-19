from fastapi import APIRouter, status

from app.core.email import EmailSession
from app.core.response_schema import IResponse
from app.modules.email.controllers import EmailController
from app.modules.email.schemas import EmailBase

router = APIRouter()



@router.post("/", status_code=status.HTTP_200_OK, response_model=IResponse)
async def send_email(email_session: EmailSession, email: EmailBase):
    return await EmailController.send_email(email_session, email)

@router.post("/test-bill", status_code=status.HTTP_200_OK, response_model=IResponse)
async def send_water_bill(
    email_session: EmailSession, 
    email: EmailBase, 
    name: str = "Usuario", 
    reading: float = 0.0, 
    date: str = "2026-01-01", 
    months: int = 0
):
    return await EmailController.send_water_bill_email(email_session, email, name, reading, date, months)
