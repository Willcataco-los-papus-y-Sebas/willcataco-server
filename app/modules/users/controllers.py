from pydantic import EmailStr

from app.core.enums import UserRole
from app.core.response_schema import IResponse
from fastapi import HTTPException
from app.modules.users.services import UserService
from app.core.database import SessionDep
from app.modules.users.model.schemas import UserBase, UserPatch


class UserController:
    @staticmethod
    async def delete_user(id: int, session: SessionDep):
        user = await UserService.get_user_by_id(session, id)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        await UserService.delete_user(session, id)
        response = IResponse(detail="user deleted", status_code=200)
        return response

    @staticmethod
    async def patch_information_user(
        id: int, session: SessionDep, user_info: UserPatch
    ):
        user = await UserService.get_user_by_id(session, id)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        user_email = await UserService.get_user_by_email(session, user_info.email)
        user_username = await UserService.get_user_by_username(
            session, user_info.username
        )
        if user_email or user_username:
            raise HTTPException(
                status_code=400, detail="email or username already exist"
            )
        user_patched = await UserService.patch_information_user(session, id, user_info)
        response = IResponse(detail="User patched", status_code=200, data=user_patched)
        return response

    @staticmethod
    async def create_user(session: SessionDep, user_info: UserBase):
        user_email = await UserService.get_user_by_email(session, user_info.email)
        user_username = await UserService.get_user_by_username(
            session, user_info.username
        )
        if user_email or user_username:
            raise HTTPException(
                status_code=400, detail="email or username already exist"
            )
        user = await UserService.create_user(session, user_info)
        response = IResponse(detail="User Created", status_code=201, data=user)
        return response

    #modificar
    @staticmethod
    async def create_user_mesa(session: SessionDep, user_info: UserBase):
        if user_info.role != UserRole.MEMBER:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user_email = await UserService.get_user_by_email(session, user_info.email)
        user_username = await UserService.get_user_by_username(
            session, user_info.username
        )
        if user_email or user_username:
            raise HTTPException(
                status_code=400, detail="email or username already exist"
            )
        user = await UserService.create_user(session, user_info)
        response = IResponse(detail="User Created", status_code=201, data=user)
        return response

    @staticmethod
    async def read_user(id: int, session: SessionDep):
        user = await UserService.get_user_by_id(session, id)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        response = IResponse(detail="user found", status_code=200, data=user)
        return response

    @staticmethod
    async def search_user(
        email: EmailStr | None, username: str | None, session: SessionDep
    ):
        if not email and not username:
            raise HTTPException(status_code=400, detail="Bad request")
        if email:
            user = await UserService.get_user_by_email(session, email)
            if not user:
                raise HTTPException(status_code=404, detail="user not found")
            response = IResponse(detail="user found", status_code=200, data=user)
            return response
        if username:
            user = await UserService.get_user_by_username(session, username)
            if not user:
                raise HTTPException(status_code=404, detail="user not found")
            response = IResponse(detail="user found", status_code=200, data=user)
            return response
