from sqlalchemy import select,func

from app.core.database import SessionDep
from app.modules.members.model.models import Member
from app.modules.members.model.schemas import (
   MemberBase,
   MemberResponse,
)

class MemberService:
    @staticmethod
    async def get_member_by_id(session: SessionDep, id: int):
        try:
            result = await session.execute(select(Member).where(Member.id == id))
            member_orm = result.scalars().one_or_none()
            return MemberResponse.model_validate(member_orm) if member_orm else None
        except Exception:
            await session.rollback()
            raise


    @staticmethod
    async def get_member_by_ci(session: SessionDep, ci: str):
        try:
            result = await session.execute(select(Member).where(Member.ci == ci))
            member_orm  = result.scalars().one_or_none()
            return MemberResponse.model_validate(member_orm) if member_orm else None
        except Exception:
            await session.rollback()
            raise

    
    @staticmethod
    async def get_member_by_last_name(session: SessionDep, last_name: str):
        try:
            member = await session.execute(select(Member).where(Member.last_name == last_name))
            member_orm = member.scalars().one_or_none()
            return MemberResponse.model_validate(member_orm) if member_orm else None
        except Exception:
            await session.rollback()
            raise


    @staticmethod
    async def create_member(session: SessionDep, member_info: MemberBase, user_ids: int):
        try:
            new_member = Member(
                name = member_info.name,
                last_name = member_info.last_name,
                user_id = user_ids,
                ci = member_info.ci,
                phone = member_info.phone
            )
            session.add(new_member)
            await session.commit()
            await session.refresh(new_member)
            return MemberResponse.model_validate(new_member)
        except Exception:
            await session.rollback()
            raise

    
    @staticmethod
    async def patch_infomation_member(session: SessionDep, id: int, member_info: MemberBase):
        try:
            member = await session.execute(select(Member).where(Member.id == id))
            member_orm = member.scalars().one()
            if member_info.name is not None:
                member_orm.name = member_info.name
            if member_info.last_name is not None:
                member_orm.last_name = member_info.last_name
            if member_info.ci is not None:
                member_orm.ci = member_info.ci
            if member_info.phone is not None:
                member_orm.phone = member_info.phone
            await session.commit()
            await session.refresh(member_orm)
            return MemberResponse.model_validate(member_orm)
        except Exception:
            await session.rollback()
            raise
    

    @staticmethod
    async def delete_member(session: SessionDep, id: int):
        try:
            member = await session.execute(select(Member).where(Member.id == id))
            member_orm = member.scalars().one()
            member_orm.deleted_at = func.now()
            await session.commit()
            await session.refresh(member_orm)
            return MemberResponse.model_validate(member_orm)
        except Exception:
            await session.rollback()
            raise

