from fastapi import APIRouter, Depends, status

from app.core.database import SessionDep
from app.core.dependencies import RequireRoles
from app.core.enums import UserRole
from app.core.response_schema import IResponse
from app.modules.water_meters.actions.controllers import ActionController
from app.modules.water_meters.actions.model.schemas import ActionCreate, ActionPatch

router = APIRouter()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))],
)
async def create_action(session: SessionDep, action_info: ActionCreate):
    return await ActionController.create_action(session, action_info)

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))],
)
async def read_action(id: int, session: SessionDep):
    return await ActionController.read_action(id, session)

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))],
)
async def read_all_actions(session: SessionDep, skip: int = 0, limit: int = 100):
    return await ActionController.read_all_actions(session, skip, limit)

@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN, UserRole.STAFF))],
)
async def update_action(id: int, session: SessionDep, action_info: ActionPatch):
    return await ActionController.update_action(id, session, action_info)

@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse,
    dependencies=[Depends(RequireRoles(UserRole.ADMIN))],
)
async def delete_action(id: int, session: SessionDep):
    return await ActionController.delete_action(id, session)
