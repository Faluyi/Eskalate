from pydantic import BaseModel, EmailStr
from typing import Optional


class CompanyCreate(BaseModel):
    name: str
    email: EmailStr
    website: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None