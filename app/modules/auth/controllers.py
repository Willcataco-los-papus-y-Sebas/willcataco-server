from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import SessionDep
from app.modules.users.services import UserService
from app.modules.auth.jwt import JWTokens

class AuthController:
    @staticmethod
    async def login_token(
        session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
        ctrl_user = await UserService.get_user_by_email(session, email=form_data.username)
        if not ctrl_user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        user = await UserService.authenticate_user(
            session, email=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        token = JWTokens.create_access_token(user.user_id)
        return token
