from datetime import datetime
from pydantic import BaseModel, ConfigDict

class WaterMeterBase(BaseModel):
    action_id: int
    water_reading: float

class WaterMeterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    action_id: int
    water_reading: float
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

class WaterMeterPatch(BaseModel):
    action_id: int | None = None
    water_reading: float | None = None