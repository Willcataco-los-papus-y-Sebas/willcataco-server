from pydantic import BaseModel, EmailStr

class EmailBase(BaseModel):
    recipient: EmailStr
    subject: str

class WaterBillEmailParams(BaseModel):
    recipient: EmailStr
    subject: str
    name: str
    reading_value: float
    date: str
    months_owed: int