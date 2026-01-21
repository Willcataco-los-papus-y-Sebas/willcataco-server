from pydantic import BaseModel, EmailStr, Field

from datetime import datetime
from decimal import Decimal

class EmailBase(BaseModel):
    recipient: EmailStr
    subject: str

class EmailWaterReceiptBase(BaseModel):
    name_member: str
    last_name_member: str
    ci_member: str
    id_payment: int
    water_reading: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    date_created: datetime
    date_updated: datetime
    amount: Decimal = Field(ge=0, max_digits=10, decimal_places=2)