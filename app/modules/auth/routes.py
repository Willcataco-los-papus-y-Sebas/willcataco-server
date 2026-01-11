from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import SessionDep
from app.core.dependencies import (
    CurrentUserFlexible,
    CurrentUserFromCookie,
    CurrentUserFromRefreshToken,
)
from app.core.email import EmailSession
from app.core.response_schema import IResponse
from app.modules.auth.controllers import AuthController
from app.modules.auth.schemas import (
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    RecoveryUser,
    RefreshResponse,
    TokenResponse,
)
from app.modules.users.model.schemas import UserResponse

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return await AuthController.login_token(session, form_data)


@router.post("/login", response_model=LoginResponse)
async def login(response: Response, session: SessionDep, credentials: LoginRequest):
    return await AuthController.login_with_cookie(response, session, credentials)


@router.get("/me", response_model=UserResponse)
async def get_me(user: CurrentUserFlexible):
    return await AuthController.get_current_user(user)


@router.post("/refresh", response_model=RefreshResponse)
async def refresh(
    response: Response, session: SessionDep, user: CurrentUserFromRefreshToken
):
    return await AuthController.refresh_token(response, session, user)


@router.post("/logout", response_model=LogoutResponse)
async def logout(response: Response):
    return await AuthController.logout(response)


@router.post("/recovery", response_model=IResponse)
async def recovery_account(
    email: RecoveryUser, session: SessionDep, session_email: EmailSession
):
    return await AuthController.recovery_account(email, session, session_email)
