from fastapi import APIRouter, Depends, status

from app.core.database import SessionDep
from app.core.dependencies import RequireRoles, CurrentUserFlexible
from app.core.enums import UserRole
from app.core.response_schema import IResponse
from app.modules.stats.controllers import StatsController

router = APIRouter()

@router.get(
    "/members",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))]
)
async def get_member_stats(
    session: SessionDep, 
    curr_user: CurrentUserFlexible = Depends()
):
    return await StatsController.get_member_stats(session, curr_user)