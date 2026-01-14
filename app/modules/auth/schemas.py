from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from app.core.enums import UserRole


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RecoveryUser(BaseModel):
    url : str
    email : EmailStr

class ResetPassword(BaseModel):
    first : str
    second : str


class InternalLoginRequest(BaseModel):
    username: str = Field(..., min_length=1)


class AuthMeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    role: UserRole
    scope: str | None


class InternalLoginRequest(BaseModel):
    username: str = Field(..., min_length=1)