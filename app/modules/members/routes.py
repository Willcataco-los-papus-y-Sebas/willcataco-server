from fastapi import APIRouter, status

from app.core.response_schema import IResponse
from app.modules.members.controllers import MemberController
from app.core.database import SessionDep
from app.modules.members.model.schemas import (MemberBase, MemberPatch)
from app.modules.users.model.schemas import (UserPatch)


router = APIRouter()

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = IResponse)
async def create_member(session: SessionDep, member_info: MemberBase):
    return await MemberController.create_member(session, member_info) 

@router.get("/{id}", status_code = status.HTTP_200_OK, response_model = IResponse)
async def read_member(id: int, session: SessionDep):
    return await MemberController.read_member(id, session)

@router.patch("{id}", status_code=status.HTTP_200_OK, response_model = IResponse)
async def patch_info_member(session: SessionDep, id: int, member_info: MemberPatch, user_info: UserPatch):
    return await MemberController.patch_info_member(session, id, member_info, user_info)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model= IResponse)
async def delete_member(session: SessionDep, id: int):
    return await MemberController.delete_member(session, id)