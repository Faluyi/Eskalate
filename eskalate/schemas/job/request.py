from pydantic import BaseModel
from typing import Optional
from enum import Enum

class JobStatus(str, Enum):
    open = "open"
    closed = "closed"
    draft = "draft"


class JobCreate(BaseModel):
    title: str
    description: str
    location: Optional[str] = None
    status: JobStatus = JobStatus.open

