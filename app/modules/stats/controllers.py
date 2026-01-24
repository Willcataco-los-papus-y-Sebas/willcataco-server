from fastapi import HTTPException, status
from app.core.database import SessionDep
from app.core.response_schema import IResponse
from app.modules.stats.services import StatsService
from app.core.dependencies import CurrentUserFlexible
from app.core.enums import UserRole

class StatsController:
    @staticmethod
    async def get_member_stats(session: SessionDep, curr_user: CurrentUserFlexible):
        if curr_user.role not in [UserRole.ADMIN, UserRole.STAFF]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges"
            )

        stats_data = await StatsService.get_member_stats(session)
        
        return IResponse(
            detail="Member statistics retrieved successfully",
            status_code=200,
            data=stats_data
        )