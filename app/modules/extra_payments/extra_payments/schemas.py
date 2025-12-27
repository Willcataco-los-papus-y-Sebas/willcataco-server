from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ExtraPaymentBase(BaseModel):
    name: str
    description: Optional[str] = None
    amount: Decimal = Field(..., ge=0, decimal_places=2)
    is_active: bool = True


class ExtraPaymentCreate(ExtraPaymentBase):
    pass


class ExtraPaymentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    is_active: Optional[bool] = None


class ExtraPaymentResponse(ExtraPaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
