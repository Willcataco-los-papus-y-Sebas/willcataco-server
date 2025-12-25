from datetime import datetime

from pydantic import BaseModel, Field, NonNegativeFloat, ConfigDict
from app.core.enums import PaymentStatus

class WaterPaymentBase(BaseModel):
    member_id: int
    meter_id: int


class WaterPaymentResponse(WaterPaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: NonNegativeFloat = Field(decimal_places=2)
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
