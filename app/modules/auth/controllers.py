from typing import Annotated

from fastapi import Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import config
from app.core.enums import UserRole
from app.core.database import SessionDep
from app.core.dependencies import CurrentUserFlexible, CurrentUserFromCookie, CurrentUserFromRefreshToken
from app.core.email import EmailSession
from app.core.response_schema import IResponse
from app.modules.auth.jwt import JWTokens
from app.modules.auth.schemas import LoginRequest, RecoveryUser, ResetPassword
from app.modules.email.schemas import EmailBase
from app.modules.email.services import EmailService
from app.modules.users.services import UserService


class AuthController:
    @staticmethod
    async def login_token(
        session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
        user = await UserService.authenticate_user(
            session, username=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(status_code=400, detail="Bad request")
        token = JWTokens.create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}

    @staticmethod
    async def login_with_cookie(
        response: Response, session: SessionDep, credentials: LoginRequest
    ):
        user = await UserService.authenticate_user(
            session, username=credentials.username, password=credentials.password
        )
        if not user:
            raise HTTPException(
                status_code=401, detail="Incorrect username or password"
            )
        
        user_orm = await UserService.get_user_orm_by_id(session, user.id)
        if not user_orm or not user_orm.member:
            raise HTTPException(status_code=403, detail="User must have a member record to use this login")

        access_token = JWTokens.create_access_token(str(user.id), user.role, "member")
        refresh_token = JWTokens.create_refresh_token(str(user.id), user.role, "member")

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            path="/",
            max_age=config.token_time_expire * 60,
            domain=None,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            path="/",
            max_age=config.refresh_token_time_expire * 60,
            domain=None,
        )

        return IResponse(detail="Login successful", status_code=200)

    @staticmethod
    async def get_current_user(user: CurrentUserFlexible, access_token: str | None):
        scope = None
        if access_token:
            try:
                payload = JWTokens.decode_access_payload(access_token)
                scope = payload.get("scope")
            except Exception:
                scope = None
        
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "scope": scope,
        }
        return IResponse(detail="Current user", status_code=200, data=user_dict)

    @staticmethod
    async def refresh_token(
        response: Response,
        session: SessionDep,
        user: CurrentUserFromRefreshToken,
        refresh_token: str | None,
    ):
        if not refresh_token:
            raise HTTPException(status_code=401, detail="No refresh token provided")

        payload = JWTokens.decode_refresh_payload(refresh_token)
        scope = payload.get("scope")
        role = payload.get("role")
        sub = payload.get("sub")
        if str(user.id) != str(sub):
            raise HTTPException(status_code=401, detail="Token subject mismatch")

        token = JWTokens.create_access_token(str(user.id), role, scope)

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            path="/",
            max_age=config.token_time_expire * 60,
            domain=None,
        )

        return IResponse(detail="Token refreshed", status_code=200)

    @staticmethod
    async def request_internal_login(request: Request, username: str, session: SessionDep, session_email: EmailSession):
        user = await UserService.get_user_by_username(session, username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.role not in (UserRole.ADMIN, UserRole.STAFF):
            raise HTTPException(status_code=403, detail="User must be admin or staff")

        token, jti, expires_at = JWTokens.create_internal_request_token(str(user.id), user.role)

        try:
            from app.modules.auth.internal_tokens import InternalTokenStore
            InternalTokenStore.register(jti, expires_at)
        except Exception:
            pass

        origin = request.headers.get("origin") or request.headers.get("referer", "").rstrip("/")
        
        url = f"{origin}/admin/login?token={token}"
        email_base = EmailBase(
            recipient=user.email,
            subject="Solicitud de acceso interno",
        )
        expire_minutes = getattr(config, "internal_token_time_expire", 10)
        
        try:
            await EmailService.send_internal_login_email(session_email, email_base, url, expire_minutes)
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to send email. Please check SMTP configuration: {str(e)}"
            )

        return IResponse(detail="Internal login requested", status_code=200)

    @staticmethod
    async def internal_login(response: Response, session: SessionDep, token: str):
        payload = JWTokens.decode_internal_request_token(token)
        sub = payload.get("sub")
        role = payload.get("role")
        jti = payload.get("jti")

        try:
            from app.modules.auth.internal_tokens import InternalTokenStore
            if not InternalTokenStore.consume(jti):
                raise HTTPException(status_code=401, detail="Token invalid or already used")
        except HTTPException:
            raise
        except Exception:
            pass

        user = await UserService.get_user_by_id(session, int(sub))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.role not in (UserRole.ADMIN, UserRole.STAFF):
            raise HTTPException(status_code=403, detail="User must be admin or staff")

        access_token = JWTokens.create_access_token(str(user.id), user.role, "internal")
        refresh_token = JWTokens.create_refresh_token(str(user.id), user.role, "internal")

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            path="/",
            max_age=config.token_time_expire * 60,
            domain=None,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            path="/",
            max_age=config.refresh_token_time_expire * 60,
            domain=None,
        )

        return IResponse(detail="Internal login successful", status_code=200)

    @staticmethod
    async def logout(response: Response):
        response.delete_cookie(
            key="access_token",
            path="/",
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            domain=None,
        )
        response.delete_cookie(
            key="refresh_token",
            path="/",
            httponly=True,
            secure=config.cookie_secure,
            samesite=config.cookie_samesite,
            domain=None,
        )

        return IResponse(detail="Logged out successfully", status_code=200)

    @staticmethod
    async def forgot_account(
        info_recovery: RecoveryUser, session: SessionDep, session_email: EmailSession
    ):
        user = await UserService.get_user_by_email(session, info_recovery.email)
        if user:
            reset_token = JWTokens.create_token_reset(user.id)
            url = f"{info_recovery.url}/password/reset?token={reset_token}"
            email_base = EmailBase(
                recipient=info_recovery.email,
                subject="Recuperacion/reset de cuenta en wilcataco",
            )
            await EmailService.send_reset_pass_email(session_email, email_base, url)
        return IResponse(detail="email received", status_code=200)

    @staticmethod
    async def reset_password(token: str, passwords: ResetPassword, session: SessionDep):
        if passwords.first != passwords.second:
            raise HTTPException(detail="passwords must be equals", status_code=401)
        user_id = JWTokens.decode_reset_token(token)
        user = await UserService.reset_password(session, user_id, passwords.first)
        if not user:
            raise HTTPException(detail="password dont updated", status_code=400)
        return IResponse(detail="password updated successfully", status_code=200)
