from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from app.core.enums import ActionStatus

class ActionBase(BaseModel):
    member_id: int
    street_id: int
    total_price: Decimal = Field(ge=0, decimal_places=2)

class ActionCreate(ActionBase):
    pass

class ActionPatch(BaseModel):
    member_id: int | None = None
    street_id: int | None = None
    total_price: Decimal | None = Field(None, ge=0, decimal_places=2)
    status: ActionStatus | None = None

class ActionResponse(ActionBase):
    id: int
    status: ActionStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
