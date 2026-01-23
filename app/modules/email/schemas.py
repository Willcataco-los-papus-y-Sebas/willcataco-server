from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class EmailBase(BaseModel):
    recipient: EmailStr
    subject: str

class WaterBillEmailParams(EmailBase):
    name: str
    reading_value: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    date: datetime
    months_owed: int = Field(ge=0)