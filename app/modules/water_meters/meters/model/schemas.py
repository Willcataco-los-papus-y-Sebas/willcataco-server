from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MeterBase(BaseModel):
    water_meter_id: int
    water_reading: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    observation: str | None = None
    photo_path: str


class MeterResponse(MeterBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    past_water_reading: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class MeterPatch(BaseModel):
    water_reading: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    observation: str | None = None
    photo_path: str
