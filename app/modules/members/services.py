from sqlalchemy import (
    func, 
    select, 
    or_, 
    and_, 
    extract
)
from sqlalchemy.orm import selectinload

from app.core.database import SessionDep
from app.modules.members.model.models import Member
from app.modules.members.model.schemas import (
    MemberBase,
    MemberPatch,
    MemberResponse,
)
from app.modules.users.model.models import User


class MemberService:
    @staticmethod
    async def get_member_by_user_id(session: SessionDep, user_id: int):
        try:
            member = await session.execute(
                select(Member).where(Member.user_id == user_id)
            )
            member_orm = member.scalar_one_or_none()
            if not member_orm:
                return None
            return MemberResponse.model_validate(member_orm)
        except Exception:
            raise

    @staticmethod
    async def get_by_phone(session: SessionDep, phone: str):
        try:
            member = await session.execute(
                select(Member).where(Member.phone == phone).where(User.is_active)
            )
            member_orm = member.scalar_one_or_none()
            if not member_orm:
                return None
            return MemberResponse.model_validate(member_orm)
        except Exception:
            raise

    @staticmethod
    async def get_member_by_id(session: SessionDep, id: int):
        try:
            result = await session.execute(
                select(Member).join(User).where(Member.id == id).where(User.is_active)
            )
            member_orm = result.scalars().one_or_none()
            return MemberResponse.model_validate(member_orm) if member_orm else None
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_member_by_ci(session: SessionDep, ci: str):
        try:
            result = await session.execute(
                select(Member)
                .join(User)
                .where(Member.ci == ci)
                .where(User.is_active)
            )
            member_orm = result.scalars().one_or_none()
            return MemberResponse.model_validate(member_orm) if member_orm else None
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def search_full_name(
        session: SessionDep, 
        fullname: str, 
        year: int | None, 
        month: int | None, 
        limit: int, 
        offset: int
    ):
        try:
            terms = fullname.strip().split()
            and_conditions = []

            for term in terms:
                and_conditions.append(
                or_(
                    Member.name.ilike(f"{term}%"),
                    Member.last_name.ilike(f"{term}%"),
                    Member.name.ilike(f"% {term}%"),
                    Member.last_name.ilike(f"% {term}%")
                )
                )
                    
                condition = and_(*and_conditions)
            
            condition_date = MemberService.get_query_date(year, month)

            query = (
                select(Member)
                .join(User)
                .where(User.is_active)
                .where(condition)
            )

            if condition_date is not None:
                query = query.where(condition_date)

            query = query.order_by(Member.last_name, Member.name).limit(limit).offset(offset)
            members = await session.execute(query)
            members_orm = members.scalars().all()
            return [MemberResponse.model_validate(m) for m in members_orm]
        except Exception:
            raise

    @staticmethod
    async def create_member(
        session: SessionDep, member_info: MemberBase
    ):
        try:
            new_member = Member(
                name=member_info.name,
                last_name=member_info.last_name,
                ci=member_info.ci,
                phone=member_info.phone,
                user_id=member_info.user_id,
            )
            session.add(new_member)
            await session.commit()
            await session.refresh(new_member)
            return MemberResponse.model_validate(new_member)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def patch_infomation_member(
        session: SessionDep, id: int, member_info: MemberPatch
    ):
        try:
            member = await session.execute(select(Member).where(Member.id == id))
            member_orm = member.scalars().one_or_none()
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
            member = await session.execute(
                select(Member).options(selectinload(Member.user)).where(Member.id == id)
            )
            member_orm = member.scalars().one_or_none()
            datetime = func.now()
            member_orm.deleted_at = datetime
            member_orm.user.is_active = False
            member_orm.user.deleted_at = datetime
            await session.commit()
            await session.refresh(member_orm)
            return MemberResponse.model_validate(member_orm)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_all(session: SessionDep, limit: int, offset: int):
        try:
            members = await session.execute(
                select(Member)
                .join(User)
                .where(User.is_active)
                .order_by(Member.last_name, Member.name)
                .limit(limit)
                .offset(offset)
            )
            members_orm = members.scalars().all()
            return [MemberResponse.model_validate(m) for m in members_orm]
        except Exception:
            raise

    @staticmethod
    async def get_members_by_time(
        session: SessionDep, year: int | None, month: int | None, limit: int, offset: int
    ):
        try:
            query = ( 
                select(Member)
                .join(User)
                .where(User.is_active)
            )

            date = MemberService.get_query_date(year, month)

            if date is not None:
                query = query.where(date)
            
            query = query.order_by(Member.created_at.desc()).limit(limit).offset(offset)

            members = await session.execute(query)
            members_orm = members.scalars().all()
            return [MemberResponse.model_validate(m) for m in members_orm]
        except Exception:
            raise

    @staticmethod
    def get_query_date(year: int | None, month: int | None):
        date = []
        if year:
            date.append(
                extract('year', Member.created_at) == year
            )
        if month:
            date.append(
                extract('month', Member.created_at) == month
            )
        return and_(*date) if date else None