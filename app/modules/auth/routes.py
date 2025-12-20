from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.modules.auth.controllers import AuthController
from app.core.database import SessionDep

router = APIRouter()


@router.post("/token")
async def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return await AuthController.login_token(session, form_data)
