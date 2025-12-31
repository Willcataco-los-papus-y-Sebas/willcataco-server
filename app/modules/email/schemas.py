from pydantic import BaseModel

class EmailBase(BaseModel):
    subject: str
    body: str