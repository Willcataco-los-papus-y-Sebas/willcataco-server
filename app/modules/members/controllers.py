from fastapi import HTTPException

from app.core.database import SessionDep
from app.core.enums import UserRole
from app.core.dependencies import CurrentUserFlexible
from app.core.response_schema import IResponse
from app.modules.members.model.schemas import MemberBase, MemberPatch, MemberResponse
from app.modules.members.services import MemberService
from app.modules.users.controllers import UserController
from app.modules.users.model.schemas import UserBase


class MemberController:

    @staticmethod
    async def delete_member(session: SessionDep, id: int):
        member = await MemberService.get_member_by_id(session, id)
        if not member:
            raise HTTPException(status_code=404, detail="member not found")
        await MemberService.delete_member(session, id)
        response = IResponse(detail="Member deleted", status_code=200)
        return response
    
    
    @staticmethod
    async def patch_info_member(
        session: SessionDep, id: int, member_info: MemberPatch
    ):
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
    async def create_member(
        session: SessionDep, member_info: MemberBase, current_user: CurrentUserFlexible
    ):
        member_ci = await MemberService.get_member_by_ci(session, member_info.ci)
        if member_ci:
            raise HTTPException(status_code=400, detail="Member already exist")
        generic_user = UserBase(
            username= f"{member_info.last_name}_{member_info.name}",
            email=member_info.email,
            password=member_info.ci,
            role=UserRole.MEMBER,
        )
        user = await UserController.create_user(session, generic_user, current_user)
        user_data = user.data
        member = await MemberService.create_member(session, member_info, user_data.id)
        response = IResponse(detail="Member Created", status_code=201, data=member)
        return response
    

    @staticmethod
    async def search_member(
        session: SessionDep, ci: str | None, last_name: str | None, name: str | None, limit: int , offset: int
    ):
        if not ci and not last_name and not name:
            members = await MemberService.get_all(session , limit, offset)
            response = IResponse(detail="users retrieved" , status_code=200, data=members)
            return response
        if ci:
            member = await MemberService.get_member_by_ci(session, ci)
            if not member:
                raise HTTPException(status_code=404, data="Member not found")
            response =IResponse(detail="Member found", status_code=201, data=member)
            return response
        if last_name:
            members = await MemberService.get_members_by_last_name(session, last_name, limit, offset)
            if not members:
                raise HTTPException(status_code=404, detail="Member(s) not found")
            response = IResponse[list[MemberResponse]](detail="Member(s) found", status_code=201, data=members, 
                                                       page=((offset // limit)+1), offset=offset)
            return response
        if name:
            members = await MemberService.get_members_by_name(session, name, limit, offset)
            if not members:
                raise HTTPException(status_code=404, detail="Member(s) not found")
            response = IResponse[list[MemberResponse]](detail= "Member(s) found", status_code=201, data=members, 
                                                       page=((offset // limit)+1), offset=offset)
            return response
