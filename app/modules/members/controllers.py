from fastapi import HTTPException

from app.core.database import SessionDep
from app.core.dependencies import CurrentUserFlexible
from app.core.enums import UserRole
from app.core.response_schema import IResponse
from app.modules.members.model.schemas import MemberBase, MemberPatch
from app.modules.members.services import MemberService
from app.modules.users.services import UserService


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
    async def patch_info_member(session: SessionDep, id: int, member_info: MemberPatch):
        member = await MemberService.get_member_by_id(session, id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        member_ci = await MemberService.get_member_by_ci(session, member_info.ci)
        if member_ci:
            raise HTTPException(status_code=400, detail="CI already exists")
        if member_info.phone:
            member_phone = await MemberService.get_by_phone(session, member_info.phone)
            if member_phone:
                raise HTTPException(status_code=400, detail="phone already exist")
        member_patched = await MemberService.patch_infomation_member(session, id, member_info)
        response = IResponse(
            detail="Member patched", status_code=200, data=member_patched
        )
        return response

    @staticmethod
    async def read_member(id: int, session: SessionDep):
        member = await MemberService.get_member_by_id(session, id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        response = IResponse(detail="member found", status_code=200, data=member)
        return response

    @staticmethod
    async def create_member(
        session: SessionDep, member_info: MemberBase, current_user: CurrentUserFlexible
    ):
        user= await UserService.get_user_by_id(session, member_info.user_id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        if current_user.role == UserRole.STAFF and user.role != UserRole.MEMBER :
            raise HTTPException(status_code=400, detail="staff only can create members")
        member_ci = await MemberService.get_member_by_ci(session, member_info.ci)
        if member_ci:
            raise HTTPException(status_code=400, detail="Member already exist")
        member_phone = await MemberService.get_by_phone(session, member_info.phone)
        if member_phone:
            raise HTTPException(status_code=400, detail="phone already exist")
        member_user_id = await MemberService.get_member_by_user_id(session, member_info.user_id)
        if member_user_id:
            raise HTTPException(status_code=400, detail="User already exist")
        member = await MemberService.create_member(session, member_info)
        response = IResponse(detail="Member Created", status_code=201, data=member)
        return response

    @staticmethod
    async def search_member(
        session: SessionDep,
        ci: str | None,
        full_name: str | None,
        limit: int,
        offset: int,
    ):
        if not ci and not full_name:
            members = await MemberService.get_all(session, limit, offset)
            response = IResponse(
                detail="users retrieved", status_code=200, data=members
            )
            return response
        if ci:
            member = await MemberService.get_member_by_ci(session, ci)
            if not member:
                raise HTTPException(status_code=404, detail="Member not found")
            response = IResponse(detail="Member found", status_code=200, data=member)
            return response
        if full_name:
            member = await MemberService.search_full_name(session, full_name, limit, offset)
            if not member:
                raise HTTPException(status_code=404, detail="Member(s) not found")
            response = IResponse(detail="Member(s) found", status_code=200, data=member)
            return response
  
