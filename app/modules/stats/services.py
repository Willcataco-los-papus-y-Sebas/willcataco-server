from sqlalchemy import case, func, select, union
from app.core.enums import PaymentStatus, ActionStatus
from app.core.database import SessionDep
from app.modules.members.model.models import Member
from app.modules.users.model.models import User
from app.modules.members.model.schemas import MemberStatsResponse
from app.modules.water_meters.water_payments.model.models import WaterPayment
from app.modules.extra_payments.payments.model.models import Payment as ExtraPayment
from app.modules.water_meters.actions.model.models import Action

class StatsService:
    @staticmethod
    async def get_member_stats(session: SessionDep) -> MemberStatsResponse:
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
                func.count(Member.id).label("total_members"),
                func.count(case((User.is_active, 1))).label("active_members"),
                func.count(case((~User.is_active, 1))).label("inactive_members"),
                func.count(case((Member.id.in_(select(debtors_union)), 1))).label("members_with_debt"),
                (
                    func.count(Member.id) - 
                    func.count(case((Member.id.in_(select(debtors_union)), 1)))
                ).label("members_solvent")
            ).join(User)
            result = await session.execute(query)
            stats_row = result.one()
            return MemberStatsResponse.model_validate(stats_row)
        except Exception:
            raise