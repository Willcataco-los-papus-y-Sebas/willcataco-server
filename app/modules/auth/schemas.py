from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    ok: bool = True


class LogoutResponse(BaseModel):
    ok: bool = True


class RefreshResponse(BaseModel):
    ok: bool = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RecoveryUser(BaseModel):
    url : str
    email : EmailStr
