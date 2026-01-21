from fastapi import APIRouter, Depends, status
from app.core.database import SessionDep
from app.core.dependencies import RequireRoles
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
async def get_member_stats(session: SessionDep):
    return await StatsController.get_member_stats(session)