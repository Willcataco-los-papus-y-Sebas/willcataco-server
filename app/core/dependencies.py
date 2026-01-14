from typing import Annotated

import jwt
from fastapi import Cookie, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.config import config
from app.core.database import SessionDep
from app.core.enums import UserRole
from app.modules.auth.jwt import JWTokens
from app.modules.users.model.models import User

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
oauth2_optional = OAuth2PasswordBearer(tokenUrl="/api/auth/token", auto_error=False)
TokenDep = Annotated[str, Depends(oauth2)]

async def get_current_user(session: SessionDep, token: TokenDep):
    try:
        payload = jwt.decode(
            token, config.token_key, algorithms=[config.token_algorithm]
        )
        token_data = int(payload["sub"])
    except Exception:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
    user = await session.get_one(User, token_data)
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_user_from_cookie(
    session: SessionDep,
    access_token: str | None = Cookie(None, alias="access_token")
):
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated - no token found"
        )
    
    user_id = JWTokens.decode_access_token(access_token)
    
    user = await session.get_one(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive"
        )
    
    return user


async def get_current_user_from_refresh_token(
    session: SessionDep,
    refresh_token: str | None = Cookie(None, alias="refresh_token")
):
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated - no refresh token found"
        )
    
    # Decode and validate refresh token
    user_id = JWTokens.decode_refresh_token(refresh_token)
    
    # Get user from database
    user = await session.get_one(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive"
        )
    
    return user


async def get_current_user_flexible(
    session: SessionDep,
    access_token: str | None = Cookie(None, alias="access_token"),
    auth_header: str | None = Depends(oauth2_optional)
):

    token_to_use = access_token or auth_header
    
    if not token_to_use:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    
    user_id = JWTokens.decode_access_token(token_to_use)
    
    user = await session.get_one(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive"
        )
    
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentUserFromCookie = Annotated[User, Depends(get_current_user_from_cookie)]
CurrentUserFromRefreshToken = Annotated[User, Depends(get_current_user_from_refresh_token)]
CurrentUserFlexible = Annotated[User, Depends(get_current_user_flexible)]

class RequireRoles:
    def __init__(self, *allowed_roles: UserRole):
        self.allowed_roles = allowed_roles

    def __call__(self, user: CurrentUserFlexible):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="User dont have privileges",
            )
        return user
