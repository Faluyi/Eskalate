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

class ApplicationCreate(BaseModel):
    applicant_id: str
    job_id: str
    status: Optional[ApplicationStatus] = ApplicationStatus.applied
    cover_letter: Optional[str] = None
