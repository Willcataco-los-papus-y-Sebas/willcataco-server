from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class WaterMeterBase(BaseModel):
    action_id: int
    water_reading: float = Field(..., gt=0)
class WaterMeterCreate(WaterMeterBase):
    pass

class WaterMeterPatch(BaseModel):
    action_id: int | None = None
    water_reading: float | None = Field(default=None, gt=0)

class WaterMeterResponse(WaterMeterBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None