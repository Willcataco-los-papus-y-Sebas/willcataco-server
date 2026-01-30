from fastapi import APIRouter, status

from app.core.dependencies import CurrentUserFlexible
from app.core.email import EmailSession
from app.core.response_schema import IResponse
from app.modules.email.controllers import EmailController
from app.modules.email.schemas import EmailBase, ExtraPaymentEmailParams

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=IResponse)
async def send_email(email_session: EmailSession, email: EmailBase):
    return await EmailController.send_email(email_session, email)


@router.post("/notifications/extra-payment", status_code=status.HTTP_200_OK, response_model=IResponse)
async def send_extra_payment_email(
    email_session: EmailSession,
    payment_data: ExtraPaymentEmailParams,
    user: CurrentUserFlexible,
):
    return await EmailController.send_extra_payment_email(
        email_session, payment_data, user
    )
