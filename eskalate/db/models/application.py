import enum
import uuid
from sqlalchemy import Column, String, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class ApplicationStatus(str, enum.Enum):
    applied = "Applied"
    reviewed = "Reviewed"
    interview = "Interview"
    rejected = "Rejected"
    hired = "Hired"

class Application(Base):
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    applicant_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    resume_link = Column(String(500), nullable=False)
    cover_letter = Column(String(200), nullable=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.applied)
    applied_at = Column(DateTime, default=datetime.utcnow)

    applicant = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
