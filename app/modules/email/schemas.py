from pydantic import BaseModel, EmailStr

class EmailBase(BaseModel):
    recipient: EmailStr
    subject: str