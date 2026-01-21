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
                func.count(Member.id).label("total"),
                func.count(case((User.is_active == True, 1))).label("active"),
                func.count(case((User.is_active == False, 1))).label("inactive"),
                func.count(case((Member.id.in_(select(debtors_union)), 1))).label("debt")
            ).join(User)
            result = await session.execute(query)
            stats = result.one()
            total = stats.total or 0
            debt = stats.debt or 0
            return MemberStatsResponse(
                total_members=total,
                active_members=stats.active or 0,
                inactive_members=stats.inactive or 0,
                members_with_debt=debt,
                members_solvent=total - debt
            )
        except Exception as e:
            print(f"Error calculating stats: {e}") 
            raise e