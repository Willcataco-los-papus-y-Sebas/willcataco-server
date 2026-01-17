from sqlalchemy import case, func, select, union
from sqlalchemy.orm import selectinload
from app.core.enums import PaymentStatus, ActionStatus

from app.core.database import SessionDep
from app.modules.members.model.models import Member
from app.modules.members.model.schemas import (
    MemberBase,
    MemberPatch,
    MemberResponse,
)
from app.modules.users.model.models import User

from app.modules.water_meters.water_payments.model.models import WaterPayment
from app.modules.extra_payments.payments.model.models import Payment as ExtraPayment
from app.modules.water_meters.actions.model.models import Action

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
                select(Member).join(User).where(Member.ci == ci).where(User.is_active)
            )
            member_orm = result.scalars().one_or_none()
            return MemberResponse.model_validate(member_orm) if member_orm else None
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_members_by_name(
        session: SessionDep, name: str, limit: int, offset: int
    ):
        try:
            member = await session.execute(
                select(Member)
                .join(User)
                .where(Member.name.ilike(f"%{name}%"))
                .where(User.is_active)
                .order_by(Member.last_name, Member.name)
                .limit(limit)
                .offset(offset)
            )
            member_orm = member.scalars().all()
            return [MemberResponse.model_validate(m) for m in member_orm]
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_members_by_last_name(
        session: SessionDep, last_name: str, limit: int, offset: int
    ):
        try:
            member = await session.execute(
                select(Member)
                .join(User)
                .where(Member.last_name.ilike(f"%{last_name}%"))
                .where(User.is_active)
                .order_by(Member.last_name, Member.name)
                .limit(limit)
                .offset(offset)
            )
            member_orm = member.scalars().all()
            return [MemberResponse.model_validate(m) for m in member_orm]
        except Exception:
            await session.rollback()
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
            return [MemberResponse.model_validate(mem) for mem in members_orm]
        except Exception:
            raise

    @staticmethod
    async def get_dashboard_stats(session: SessionDep) -> dict:
        try:
            debtors_water_query = select(WaterPayment.member_id).where(
                WaterPayment.status != PaymentStatus.PAID
            )

            debtors_extra_query = select(ExtraPayment.member_id).where(
                ExtraPayment.status != PaymentStatus.PAID
            )

            debtors_action_query = select(Action.member_id).where(
                Action.status != ActionStatus.PAID
            )

            debtors_union = union(
                debtors_water_query,
                debtors_extra_query,
                debtors_action_query
            ).subquery()

            query = select(
                func.count(Member.id).label("total"),
                func.count(case((User.is_active == True, 1))).label("active"),
                func.count(case((User.is_active == False, 1))).label("inactive"),
                func.count(case((Member.id.in_(select(debtors_union)), 1))).label("debt")
            ).join(User)

            result = await session.execute(query)
            stats = result.one()

            total = stats.total or 0
            debt = stats.debt or 0
            
            return {
                "total_members": total,
                "active_members": stats.active or 0,
                "inactive_members": stats.inactive or 0,
                "members_with_debt": debt,
                "members_solvent": total - debt
            }

        except Exception as e:
            print(f"Error calculating stats: {e}")
            raise e