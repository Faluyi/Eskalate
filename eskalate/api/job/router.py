from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.schemas.job import JobCreate, JobResponse
from app.schemas.base import BaseResponse
from app.controllers import job_controller

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=BaseResponse[JobResponse])
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    return job_controller.create_job(payload, db)

@router.get("/", response_model=BaseResponse[List[JobResponse]])
def list_jobs(db: Session = Depends(get_db)):
    return job_controller.list_jobs(db)

@router.get("/{job_id}", response_model=BaseResponse[JobResponse])
def get_job(job_id: str, db: Session = Depends(get_db)):
    return job_controller.get_job(job_id, db)

@router.put("/{job_id}", response_model=BaseResponse[JobResponse])
def update_job(job_id: str, payload: JobCreate, db: Session = Depends(get_db)):
    return job_controller.update_job(job_id, payload, db)

@router.delete("/{job_id}", response_model=BaseResponse[None])
def delete_job(job_id: str, db: Session = Depends(get_db)):
    return job_controller.delete_job(job_id, db)
