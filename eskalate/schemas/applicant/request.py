from pydantic import BaseModel, EmailStr
from typing import Optional, List


class ApplicantCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None