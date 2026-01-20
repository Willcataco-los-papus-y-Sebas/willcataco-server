from pydantic import BaseModel, EmailStr, Field

from datetime import datetime
from decimal import Decimal

class EmailBase(BaseModel):
    recipient: EmailStr
    subject: str

class EmailWaterReceiptBase(BaseModel):
    recipient: EmailStr
    subject: str
    name_member: str
    last_name_member: str
    ci_member: str
    id_payment: int
    water_reading: Decimal = Field(..., decimal_places=2)
    date_created: datetime
    date_updated: datetime
    amount: Decimal = Field(..., decimal_places=2)