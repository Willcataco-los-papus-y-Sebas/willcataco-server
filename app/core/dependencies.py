from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.config import config
from app.core.database import SessionDep
from app.core.enums import UserRole
from app.modules.users.model.models import User

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
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


CurrentUser = Annotated[User, Depends(get_current_user)]


class RequireRoles:
    def __init__(self, *allowed_roles: UserRole):
        self.allowed_roles = allowed_roles

    def __call__(self, user: CurrentUser):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="User dont have privileges",
            )
        return user
