import enum
import uuid
from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from eskalate.db import Base

class JobStatus(str, enum.Enum):
    draft = "Draft"
    open = "Open"
    closed = "Closed"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=False)
    location = Column(String(255), nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.draft)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
