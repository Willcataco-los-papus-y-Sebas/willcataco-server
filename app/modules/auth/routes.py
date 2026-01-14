from typing import Annotated

from fastapi import APIRouter, Depends, Response, Cookie, Request
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
    RecoveryUser,
    TokenResponse,
    ResetPassword,
    AuthMeResponse,
    InternalLoginRequest,
)
from app.modules.users.model.schemas import UserResponse

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return await AuthController.login_token(session, form_data)


@router.post("/login", response_model=IResponse[None])
async def login(response: Response, session: SessionDep, credentials: LoginRequest):
    return await AuthController.login_with_cookie(response, session, credentials)


@router.get("/me", response_model=IResponse[AuthMeResponse])
async def get_me(user: CurrentUserFlexible, access_token: str | None = Cookie(None, alias="access_token")):
    return await AuthController.get_current_user(user, access_token)


@router.post("/refresh", response_model=IResponse[None])
async def refresh(
    response: Response,
    session: SessionDep,
    user: CurrentUserFromRefreshToken,
    refresh_token: str | None = Cookie(None, alias="refresh_token"),
):
    return await AuthController.refresh_token(response, session, user, refresh_token)


@router.post("/logout", response_model=IResponse[None])
async def logout(response: Response):
    return await AuthController.logout(response)


@router.post("/forgot", response_model=IResponse)
async def forgot_account(
    info_recovery: RecoveryUser, session: SessionDep, session_email: EmailSession
):
    return await AuthController.forgot_account(info_recovery, session, session_email)


@router.post("/reset", response_model=IResponse)
async def reset_password(
    token : str , passwords : ResetPassword, session : SessionDep
):
    return await AuthController.reset_password(token , passwords, session)

@router.post("/internal/request", response_model=IResponse[None])
async def internal_request(request: Request, body: InternalLoginRequest, session: SessionDep, session_email: EmailSession):
    return await AuthController.request_internal_login(request, body.username, session, session_email)

@router.post("/internal/login", response_model=IResponse[None])
async def internal_login(token: str, response: Response, session: SessionDep):
    return await AuthController.internal_login(response, session, token)