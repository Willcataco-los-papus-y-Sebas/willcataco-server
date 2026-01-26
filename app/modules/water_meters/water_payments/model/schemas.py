from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, NonNegativeFloat, ConfigDict
from app.core.enums import PaymentStatus

class WaterPaymentBase(BaseModel):
    member_id: int
    meter_id: int


class WaterPaymentFilter(BaseModel):
    limit: int = Field(10, ge=1)
    offset: int = Field(0, ge=0)
    member_id: int | None = None
    status: PaymentStatus | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class WaterPaymentResponse(WaterPaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal = Field(ge=0, decimal_places=2)
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
