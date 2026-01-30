from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ExtraPaymentBase(BaseModel):
    name: str
    description: str | None = None
    amount: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    is_active: bool = True


class ExtraPaymentCreate(ExtraPaymentBase):
    pass


class ExtraPaymentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    amount: Decimal | None = Field(None, ge=0, max_digits=10, decimal_places=2)
    is_active: bool | None = None


class ExtraPaymentResponse(ExtraPaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
