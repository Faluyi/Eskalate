from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models
from app.schemas.job import JobCreate, JobResponse
from app.schemas.base import BaseResponse

def create_job(payload: JobCreate, db: Session) -> BaseResponse[JobResponse]:
    job = models.Job(
        title=payload.title,
        description=payload.description,
        location=payload.location,
        status=payload.status
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return BaseResponse(success=True, message="Job created", object=JobResponse.from_orm(job))

def list_jobs(db: Session) -> BaseResponse[List[JobResponse]]:
    jobs = db.query(models.Job).all()
    return BaseResponse(success=True, message="Jobs fetched", object=[JobResponse.from_orm(j) for j in jobs])

def get_job(job_id: str, db: Session) -> BaseResponse[JobResponse]:
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return BaseResponse(success=True, message="Job fetched", object=JobResponse.from_orm(job))

def update_job(job_id: str, payload: JobCreate, db: Session) -> BaseResponse[JobResponse]:
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.title = payload.title
    job.description = payload.description
    job.location = payload.location
    job.status = payload.status
    db.commit()
    db.refresh(job)

    return BaseResponse(success=True, message="Job updated", object=JobResponse.from_orm(job))

def delete_job(job_id: str, db: Session) -> BaseResponse[None]:
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()
    return BaseResponse(success=True, message="Job deleted", object=None)
