from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.core.enums import PaymentStatus

class PaymentBase(BaseModel):
    member_id: int
    extra_payment_id: int

class PaymentCreate(PaymentBase):
    pass

class PaymentPatch(BaseModel):
    member_id: int | None = None
    extra_payment_id: int | None = None
    status: PaymentStatus | None = None

class PaymentResponse(PaymentBase):
    id: int
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
