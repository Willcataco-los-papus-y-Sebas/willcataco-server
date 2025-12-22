from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import SessionDep
from app.modules.auth.jwt import JWTokens
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
            raise HTTPException(
                status_code=400, detail="Bad request"
            )
        token = JWTokens.create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}
