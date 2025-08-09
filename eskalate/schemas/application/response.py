from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ApplicationStatus(str, Enum):
    applied = "Applied"
    reviewed = "Reviewed"
    interview = "Interview"
    rejected = "Rejected"
    hired = "Hired"


class ApplicationResponse(BaseModel):
    id: str
    applicant_id: str
    job_id: str
    status: ApplicationStatus
    cover_letter: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
