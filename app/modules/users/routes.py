from fastapi import APIRouter, Depends, status
from pydantic import EmailStr

from app.core.database import SessionDep
from app.core.dependencies import CurrentUser, RequireRoles
from app.core.enums import UserRole
from app.core.response_schema import IResponse
from app.modules.users.controllers import UserController
from app.modules.users.model.schemas import UserBase, UserPatch

router = APIRouter()


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))],
)
async def delete_user(id: int, session: SessionDep):
    return await UserController.delete_user(id, session)


@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))],
)
async def patch_information_user(id: int, session: SessionDep, user_info: UserPatch):
    return await UserController.patch_information_user(id, session, user_info)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))],
)
async def create_user(
    session: SessionDep, user_info: UserBase, current_user: CurrentUser
):
    return await UserController.create_user(session, user_info, current_user)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))],
)
async def read_user(id: int, session: SessionDep):
    return await UserController.read_user(id, session)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))],
)
async def search_user(
    session: SessionDep,
    email: EmailStr | None = None,
    username: str | None = None,
):
    return await UserController.search_user(email, username, session)
