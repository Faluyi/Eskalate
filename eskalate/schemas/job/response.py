from pydantic import BaseModel
from typing import Optional
from enum import Enum


class JobStatus(str, Enum):
    open = "open"
    closed = "closed"
    draft = "draft"

    
class JobResponse(BaseModel):
    id: str
    title: str
    description: str
    location: Optional[str]
    status: JobStatus

    class Config:
        orm_mode = True