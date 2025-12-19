from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.core.enums import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8)
    role: UserRole = UserRole.MEMBER


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active : bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class UserPatch(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    role: UserRole | None = None


class UserUpdateMe(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserResetPasswordMe(BaseModel):
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
