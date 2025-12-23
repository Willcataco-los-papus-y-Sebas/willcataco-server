from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from app.core.database import SessionDep
from app.modules.water_meters.actions.model.models import Action
from app.modules.water_meters.actions.model.schemas import (
    ActionCreate,
    ActionPatch,
    ActionResponse,
)

class ActionService:
    @staticmethod
    async def get_action_by_id(session: SessionDep, id: int):
        try:
            result = await session.execute(select(Action).where(Action.id == id))
            action_orm = result.scalars().one_or_none()
            return ActionResponse.model_validate(action_orm) if action_orm else None
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_all_actions(session: SessionDep, skip: int = 0, limit: int = 100):
        try:
            result = await session.execute(
                select(Action).where(Action.deleted_at.is_(None)).offset(skip).limit(limit)
            )
            actions_orm = result.scalars().all()
            return [ActionResponse.model_validate(action) for action in actions_orm]
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def create_action(session: SessionDep, action_info: ActionCreate):
        try:
            new_action = Action(**action_info.model_dump())
            session.add(new_action)
            await session.commit()
            await session.refresh(new_action)
            return ActionResponse.model_validate(new_action)
        except IntegrityError:
            await session.rollback()
            raise ValueError("Member or Street ID not found")
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def update_action(session: SessionDep, id: int, action_info: ActionPatch):
        try:
            result = await session.execute(select(Action).where(Action.id == id))
            action_orm = result.scalars().one()
            
            update_data = action_info.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(action_orm, key, value)
                
            await session.commit()
            await session.refresh(action_orm)
            return ActionResponse.model_validate(action_orm)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def delete_action(session: SessionDep, id: int):
        try:
            result = await session.execute(select(Action).where(Action.id == id))
            action_orm = result.scalars().one()
            action_orm.deleted_at = func.now()
            await session.commit()
        except Exception:
            await session.rollback()
            raise
