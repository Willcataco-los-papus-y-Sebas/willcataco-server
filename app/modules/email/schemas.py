from pydantic import BaseModel, EmailStr

class EmailBase(BaseModel):
    recipient: EmailStr
    subject: str

class ExtraPaymentEmailParams(BaseModel):
    recipient: EmailStr
    subject: str
    name: str
    payment_date: str
    amount: float