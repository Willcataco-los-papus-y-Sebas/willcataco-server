from fastapi import HTTPException
from app.core.database import SessionDep
from app.core.response_schema import IResponse
from app.modules.water_meters.actions.model.schemas import ActionCreate, ActionPatch
from app.modules.water_meters.actions.services import ActionService

class ActionController:
    @staticmethod
    async def create_action(session: SessionDep, action_info: ActionCreate):
        action = await ActionService.create_action(session, action_info)
        return IResponse(detail="Action created", status_code=201, data=action)

    @staticmethod
    async def read_action(id: int, session: SessionDep):
        action = await ActionService.get_action_by_id(session, id)
        if not action:
            raise HTTPException(status_code=404, detail="Action not found")
        return IResponse(detail="Action found", status_code=200, data=action)

    @staticmethod
    async def read_all_actions(session: SessionDep, skip: int = 0, limit: int = 100):
        actions = await ActionService.get_all_actions(session, skip, limit)
        return IResponse(detail="Actions list", status_code=200, data=actions)

    @staticmethod
    async def update_action(id: int, session: SessionDep, action_info: ActionPatch):
        action = await ActionService.get_action_by_id(session, id)
        if not action:
            raise HTTPException(status_code=404, detail="Action not found")
        
        updated_action = await ActionService.update_action(session, id, action_info)
        return IResponse(detail="Action updated", status_code=200, data=updated_action)

    @staticmethod
    async def delete_action(id: int, session: SessionDep):
        action = await ActionService.get_action_by_id(session, id)
        if not action:
            raise HTTPException(status_code=404, detail="Action not found")
            
        await ActionService.delete_action(session, id)
        return IResponse(detail="Action deleted", status_code=200)
