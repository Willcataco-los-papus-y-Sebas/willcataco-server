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
from app.modules.water_meters.meters.model.models import Meter
from app.modules.water_meters.water_payments.model.models import WaterPayment
from app.modules.extra_payments.payments.model.models import Payment
from app.core.enums import PaymentStatus

from datetime import date, datetime, time, timedelta

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
            condition_date = MemberService.__get_query_date(year, month)

            query = (
                select(Member)
                .join(User)
                .where(User.is_active)
                .where(condition)
            )

            if condition_date is not None:
                query = query.where(condition_date)

            query = (
                query
                .order_by(Member.last_name, Member.name)
                .limit(limit)
                .offset(offset)
            )

            members = await session.execute(query)
            members_orm = members.scalars().all()
            return [MemberResponse.model_validate(m) for m in members_orm]
        except Exception:
            raise

    @staticmethod
    async def create_member(session: SessionDep, member_info: MemberBase):
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
            member = await session.execute(
                select(Member).where(Member.id == id)
            )
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
                select(Member).where(Member.id == id)
            )
            member_orm = member.scalars().one_or_none()
            datetime = func.now()
            member_orm.deleted_at = datetime
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
    async def get_member_with_details(session: SessionDep, id: int):
        try:
            result = await session.execute(
                select(Member)
                .join(User)
                .options(
                    selectinload(Member.water_payments).selectinload(WaterPayment.meter),
                    selectinload(Member.payments).selectinload(Payment.extra_payment)
                )
                .where(Member.id == id)
                .where(User.is_active)
            )
            member_orm = result.scalars().one_or_none()
            return member_orm 
        except Exception:
            raise

    @staticmethod
    async def get_new_members_between_dates(
        session: SessionDep,
        start_date: date,
        end_date: date,
    ) -> list[MemberResponse]:
        try:
            start_dt = datetime.combine(start_date, time.min)
            end_exclusive = datetime.combine(end_date + timedelta(days=1), time.min)

            result = await session.execute(
                select(Member)
                .join(User)
                .where(User.is_active)
                .where(Member.deleted_at.is_(None))
                .where(Member.created_at >= start_dt)
                .where(Member.created_at < end_exclusive)
                .order_by(Member.created_at, Member.last_name, Member.name)
            )

            members_orm = result.scalars().all()
            return [MemberResponse.model_validate(m) for m in members_orm]

        except Exception:
            raise
    
    @staticmethod 
    async def get_members_water_payments(
        session: SessionDep, start_date: date, end_date: date
    ):
        try:
            start_dt = datetime.combine(start_date, time.min)
            if end_date.month == 12:
                end_next_month = end_date.replace(year=end_date.year + 1, month=1)
            else:
                end_next_month = end_date.replace(month=end_date.month + 1)

            end_exclusive = datetime.combine(end_next_month - timedelta(days=1), time.min)

            members = await session.execute(
                select(Member).
                join(User).
                join(WaterPayment).
                options(
                    selectinload(Member.water_payments).
                    selectinload(WaterPayment.meter).
                    selectinload(Meter.water_meter)
                ).
                where(User.is_active).
                where(and_(WaterPayment.created_at >= start_dt, 
                           WaterPayment.created_at <= end_exclusive)
                ).
                distinct().
                order_by(Member.last_name, Member.name)
            )

            members_orm = members.scalars().all()
            print(members_orm)

            period = []

            while start_dt < end_exclusive:
                period.append({
                    "year": start_dt.year,
                    "month": start_dt.month,
                    "members": []
                })

                if start_dt.month == 12:
                    start_dt = start_dt.replace(
                        year= start_dt.year +1, 
                        month= 1
                    )
                else:
                    start_dt= start_dt.replace(month= start_dt.month +1)

            for period_data in period:
                year = period_data["year"]
                month = period_data["month"]
                period_data["members"] = []
                for member in members_orm:
                    month_paid = None
                    for payment in member.water_payments:
                        if(payment.created_at.year == year and
                           payment.created_at.month == month):
                            month_paid = payment
                            is_paid = month_paid.status == PaymentStatus.PAID
                            period_data["members"].append({
                                "name": member.name,
                                "last_name": member.last_name,
                                "meter_id": month_paid.meter.water_meter.id,
                                "consumption": month_paid.meter.water_reading - month_paid.meter.past_water_reading,
                                "amount": month_paid.amount,
                                "charge_date": month_paid.created_at.strftime("%d/%m/%Y"),
                                "payment_date": month_paid.updated_at.strftime("%d/%m/%Y %H:%M") if is_paid else None,
                                "status": month_paid.status.value
                            })
                            res = {
                                "end_date": end_exclusive,
                                "period": period
                            }
            return res
        except Exception:
            raise 

    @staticmethod
    async def get_members_by_time(
        session: SessionDep,
        year: int | None,
        month: int | None,
        limit: int,
        offset: int
    ):
        try:
            query = (
                select(Member)
                .join(User)
                .where(User.is_active)
            )

            date_condition = MemberService.__get_query_date(year, month)

            if date_condition is not None:
                query = query.where(date_condition)

            query = (
                query
                .order_by(Member.created_at.desc())
                .limit(limit)
                .offset(offset)
            )

            members = await session.execute(query)
            members_orm = members.scalars().all()
            return [MemberResponse.model_validate(m) for m in members_orm]
        except Exception:
            raise

    @staticmethod
    def __get_query_date(year: int | None, month: int | None):
        conditions = []

        if year:
            conditions.append(extract('year', Member.created_at) == year)
        if month:
            conditions.append(extract('month', Member.created_at) == month)

        return and_(*conditions) if conditions else None
