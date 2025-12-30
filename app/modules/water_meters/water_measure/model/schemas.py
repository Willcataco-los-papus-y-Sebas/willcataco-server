from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class WaterMeterBase(BaseModel):
    action_id: int
    water_reading: Decimal = Field(..., decimal_places=2)


class WaterMeterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    action_id: int
    water_reading: Decimal = Field(..., decimal_places=2)
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class WaterMeterPatch(BaseModel):
    action_id: int | None = None
    water_reading: Decimal | None = Field(default=None, decimal_places=2)
