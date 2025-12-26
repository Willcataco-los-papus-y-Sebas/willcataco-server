from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ExtraPaymentBase(BaseModel):
    name: str
    description: Optional[str] = None
    amount: float
    is_active: bool = True


class ExtraPaymentCreate(ExtraPaymentBase):
    pass


class ExtraPaymentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    is_active: Optional[bool] = None


class ExtraPaymentResponse(ExtraPaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
