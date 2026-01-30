from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class EmailBase(BaseModel):
    recipient: EmailStr
    subject: str

class ExtraPaymentEmailParams(EmailBase):
    name: str
    description: str
    payment_date: datetime
    amount: Decimal = Field(ge=0, decimal_places=2)