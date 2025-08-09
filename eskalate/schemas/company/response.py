from pydantic import BaseModel, EmailStr
from typing import Optional


class CompanyResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    website: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None

    class Config:
        orm_mode = True
