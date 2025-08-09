from pydantic import BaseModel, EmailStr
from typing import Optional, List

from eskalate.db.models.application import Application
from eskalate.db.models.job import Job


class ApplicantResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    jobs: Optional[List[Job]] = None
    applications: Optional[List[Application]] = None

    class Config:
        from_attributes = True
