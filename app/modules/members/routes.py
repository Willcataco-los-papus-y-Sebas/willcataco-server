from fastapi import APIRouter, Depends, Query, status

from app.core.database import SessionDep
from app.core.dependencies import RequireRoles, CurrentUserFlexible
from app.core.enums import UserRole
from app.core.response_schema import IResponse
from app.modules.members.controllers import MemberController
from app.modules.members.model.schemas import MemberBase, MemberPatch

router = APIRouter()

@router.post(
    "/", 
    status_code = status.HTTP_201_CREATED, 
    response_model = IResponse, 
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))]
)
async def create_member(session: SessionDep, member_info: MemberBase, current_user: CurrentUserFlexible):
    return await MemberController.create_member(session, member_info, current_user) 

@router.get(
    "/", 
    status_code= status.HTTP_200_OK, 
    response_model = IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))]
)
async def search_member(
    session: SessionDep, 
    ci: str | None= None, 
    full_name : str | None = None,
    limit: int =Query(10, ge=0, le=10), 
    offset: int=Query(0, ge=0)
):
    return await MemberController.search_member(session, ci, full_name, limit, offset)

@router.get(
    "/{id}", 
    status_code = status.HTTP_200_OK, 
    response_model = IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))]
)
async def read_member(id: int, session: SessionDep):
    return await MemberController.read_member(id, session)

@router.patch(
    "/{id}", 
    status_code=status.HTTP_200_OK, 
    response_model = IResponse, 
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))]
)
async def patch_info_member(
    session: SessionDep, 
    id: int, 
    member_info: MemberPatch
):
    return await MemberController.patch_info_member(session, id, member_info)

@router.delete(
    "/{id}", 
    status_code=status.HTTP_200_OK, 
    response_model= IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))]
)
async def delete_member(session: SessionDep, id: int):
    return await MemberController.delete_member(session, id)
