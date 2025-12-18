from fastapi import APIRouter, status
from pydantic import EmailStr

from app.modules.users.controllers import UserController
from app.core.database import SessionDep
from app.modules.users.model.schemas import (
    UserBase,
    UserPatch,
    UserResetPasswordMe,
    UserUpdateMe,
)

router = APIRouter()


@router.delete("/admin/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int, session: SessionDep):
    return await UserController.delete_user(id, session)


@router.patch("/admin/{id}", status_code=status.HTTP_200_OK)
async def patch_information_user(id: int, session: SessionDep, user_info: UserPatch):
    return await UserController.patch_information_user(id, session, user_info)


@router.post("/admin", status_code=status.HTTP_201_CREATED)
async def create_user(session: SessionDep, user_info: UserBase):
    return await UserController.create_user(session, user_info)


@router.post("/mesa", status_code=status.HTTP_201_CREATED)
async def create_user_mesa(session: SessionDep, user_info: UserBase):
    return await UserController.create_user_mesa(session, user_info)


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int, session: SessionDep):
    return await UserController.get_user_by_id(id, session)


@router.get("/", status_code=status.HTTP_200_OK)
async def search_user(
    session: SessionDep,
    email: EmailStr | None = None,
    username: str | None = None,
):
    return await UserController.search_user(email, username, session)


@router.patch("/password", status_code=status.HTTP_200_OK)
async def change_password(session: SessionDep, info_user: UserResetPasswordMe):
    return await UserController.change_password(session, info_user)


@router.patch("/", status_code=status.HTTP_200_OK)
async def change_information(session: SessionDep, info_user: UserUpdateMe):
    return await UserController.change_information(session, info_user)
