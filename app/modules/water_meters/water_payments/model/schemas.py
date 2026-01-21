from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import PaymentStatus


class WaterPaymentBase(BaseModel):
    member_id: int
    meter_id: int


class WaterPaymentResponse(WaterPaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
