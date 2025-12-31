from fastapi import APIRouter, status

from app.core.dependencies import SessionDep
from app.core.response_schema import IResponse
from app.modules.email.controllers import EmailController
from app.modules.email.schemas import EmailBase

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=IResponse)
async def send_email(session: SessionDep, email: EmailBase):
    return await EmailController.send_email(session, email)
