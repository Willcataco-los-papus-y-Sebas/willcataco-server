from app.core.database import SessionDep
from app.core.response_schema import IResponse
from app.modules.stats.services import StatsService

class StatsController:
    @staticmethod
    async def get_member_stats(session: SessionDep):
        stats_data = await StatsService.get_member_stats(session)
        return IResponse(
            detail="Member statistics retrieved successfully",
            status_code=200,
            data=stats_data
        )