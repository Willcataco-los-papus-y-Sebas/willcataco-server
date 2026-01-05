from pydantic import BaseModel, Field


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
