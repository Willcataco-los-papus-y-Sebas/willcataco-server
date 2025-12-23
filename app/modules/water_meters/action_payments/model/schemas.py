from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ActionPaymentBase(BaseModel):
    action_id: int
    amount: float

class ActionPaymentCreate(ActionPaymentBase):
    pass

class ActionPaymentPatch(BaseModel):
    amount: float | None = None

class ActionPaymentResponse(ActionPaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
