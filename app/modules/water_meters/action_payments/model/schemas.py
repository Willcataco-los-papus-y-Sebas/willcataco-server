from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ActionPaymentBase(BaseModel):
    action_id: int
    amount: Decimal = Field(ge=0, max_digits=10, decimal_places=2)


class ActionPaymentCreate(ActionPaymentBase):
    pass


class ActionPaymentPatch(BaseModel):
    action_id: int | None = None
    amount: Decimal | None = Field(None, ge=0, max_digits=10, decimal_places=2)


class ActionPaymentResponse(ActionPaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
