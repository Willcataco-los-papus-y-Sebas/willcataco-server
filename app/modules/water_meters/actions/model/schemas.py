from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.core.enums import ActionStatus

class ActionBase(BaseModel):
    member_id: int
    street_id: int
    total_price: float
    status: ActionStatus = ActionStatus.UNPAID

class ActionCreate(ActionBase):
    pass

class ActionPatch(BaseModel):
    member_id: int | None = None
    street_id: int | None = None
    total_price: float | None = None
    status: ActionStatus | None = None

class ActionResponse(ActionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
