from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MemberBase(BaseModel):
    name: str
    last_name: str
    ci: str
    phone: str
    user_id: int

class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    name: str
    last_name: str
    ci: str
    phone: str
    created_at: datetime
    updated_at: datetime 
    deleted_at: datetime | None = None

class MemberPatch(BaseModel):
    name: str | None = None
    last_name: str | None = None
    ci: str | None = None
    phone: str | None = None

class MemberStatsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_members: int
    active_members: int
    inactive_members: int
    members_with_debt: int
    members_solvent: int