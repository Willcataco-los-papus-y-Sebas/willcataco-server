from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat


class MeterBase(BaseModel):
    water_meter_id: int
    water_reading: NonNegativeFloat = Field(decimal_places=2)
    observation: str | None = None
    photo_path: str


class MeterResponse(MeterBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    past_water_reading: NonNegativeFloat = Field(decimal_places=2)
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class MeterPatch(BaseModel):
    water_reading: NonNegativeFloat = Field(decimal_places=2)
    observation: str | None = None
    photo_path: str
