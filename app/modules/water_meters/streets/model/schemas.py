from datetime import datetime

from pydantic import BaseModel, ConfigDict

class StreetBase(BaseModel):
    name: str

class StreetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None= None

class StreetPatch(BaseModel):
    name: str | None= None