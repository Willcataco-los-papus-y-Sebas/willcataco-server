from typing import Annotated

from fastapi import Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import config
from app.core.database import SessionDep
from app.core.dependencies import CurrentUserFromCookie, CurrentUserFlexible
from app.modules.auth.jwt import JWTokens
from app.modules.auth.schemas import LoginRequest, RecoveryUser
from app.modules.users.services import UserService
from app.core.email import EmailSession
from app.core.response_schema import IResponse
from app.modules.email.schemas import EmailBase
from app.modules.email.services import EmailService
class AuthController:
    @staticmethod
    async def login_token(
        session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
        user = await UserService.authenticate_user(
            session, username=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=400, detail="Bad request"
            )
        token = JWTokens.create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}

    @staticmethod
    async def login_with_cookie(
        response: Response,
        session: SessionDep,
        credentials: LoginRequest
    ):
        user = await UserService.authenticate_user(
            session, username=credentials.username, password=credentials.password
        )
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"
            )
        
        access_token = JWTokens.create_access_token(user.id)
        refresh_token = JWTokens.create_refresh_token(user.id)
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            path="/",
            max_age=config.token_time_expire * 60,
            domain=None
        )
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            path="/",
            max_age=config.refresh_token_time_expire * 60,
            domain=None
        )
        
        return {"ok": True}

    @staticmethod
    async def get_current_user(user: CurrentUserFlexible):
        return user

    @staticmethod
    async def refresh_token(
        response: Response,
        session: SessionDep,
        user: CurrentUserFromCookie
    ):
        token = JWTokens.create_access_token(user.id)
        
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            path="/",
            max_age=config.token_time_expire * 60,
            domain=None
        )
        
        return {"ok": True}

    @staticmethod
    async def logout(response: Response):
        response.delete_cookie(
            key="access_token",
            path="/",
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            domain=None
        )
        response.delete_cookie(
            key="refresh_token",
            path="/",
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            domain=None
        )
        
        return {"ok": True}
    
    @staticmethod
    async def recovery_account(email : RecoveryUser, session : SessionDep, session_email : EmailSession):
        user = await UserService.get_user_by_email(email.email, session)
        if user:
            email_base = EmailBase(
                recipient=email.email,
                subject="Recuperacion de cuenta en wilcataco",
                body=""
            )
            await EmailService.send_email(session_email, email_base)
        return IResponse(detail="email received", status_code=200)