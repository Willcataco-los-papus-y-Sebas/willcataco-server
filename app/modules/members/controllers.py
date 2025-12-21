

from app.core.response_schema import IResponse
from fastapi import HTTPException

from app.modules.members.services import MemberService
from app.modules.users.controllers import UserController

from app.core.database import SessionDep
from app.core.enums import UserRole
from app.modules.members.model.schemas import MemberBase, MemberPatch, MemberResponse
from app.modules.users.model.schemas import UserBase, UserPatch, UserResponse


class MemberController:

    @staticmethod
    async def delete_member(session: SessionDep, id: int):
        member = await MemberService.get_member_by_id(session, id)
        if not member:
            raise HTTPException(status_code=404, detail="member not found")
        await UserController.delete_user(member.user_id, session)
        await MemberService.delete_member(session, id)
        response = IResponse(detail="Member deleted", status_code=200)
        return response
    
    
    @staticmethod
    async def patch_info_member(session: SessionDep, id: int, member_info: MemberPatch):
        member = await MemberService.get_member_by_id(session, id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        member_ci = await MemberService.get_member_by_ci(session, member_info.ci)
        if member_ci:
            raise HTTPException(status_code=400, detail="CI already exists")
        member_patched = await MemberService.patch_info_member(session, id, member_info)
        response = IResponse(detail="Member patched", status_code=200, data=member_patched)
        return response
    
    
    @staticmethod
    async def read_member(id: int, session: SessionDep):
        member = await MemberService.get_member_by_id(session, id)
        if not member:
            raise HTTPException(status_code = 404, detail="Member not found")
        response = IResponse(detail="member found", status_code=200, data=member)
        return response
    

    @staticmethod
    async def create_member(session: SessionDep, member_info: MemberBase, user_info: UserBase):
        member_ci = await MemberService.get_member_by_ci(session, member_info.ci)
        if member_ci:
            raise HTTPException(status_code=400, detail="Member already exist")
        user = await UserController.create_user(session, user_info)
        member = await MemberService.create_member(session, member_info, user.id)
        response = IResponse(detail="Member Created", status_code=201, data=member)
        return response

    
