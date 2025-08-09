from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db.util import get_db
from eskalate.schemas.applicant.request import ApplicantCreate
from eskalate.schemas.applicant.response import ApplicantResponse
from eskalate.schemas.base import BaseResponse
from eskalate.api.applicant.controller import applicant_controller


router = APIRouter()

@router.post("/", response_model=BaseResponse[ApplicantResponse])
def create_applicant(payload: ApplicantCreate, db: Session = Depends(get_db)):
    return applicant_controller.create_applicant(payload, db)

@router.get("/", response_model=BaseResponse[List[ApplicantResponse]])
def list_applicants(db: Session = Depends(get_db)):
    return applicant_controller.list_applicants(db)

@router.get("/{applicant_id}", response_model=BaseResponse[ApplicantResponse])
def get_applicant(applicant_id: str, db: Session = Depends(get_db)):
    return applicant_controller.get_applicant(applicant_id, db)

@router.put("/{applicant_id}", response_model=BaseResponse[ApplicantResponse])
def update_applicant(applicant_id: str, payload: ApplicantCreate, db: Session = Depends(get_db)):
    return applicant_controller.update_applicant(applicant_id, payload, db)

@router.delete("/{applicant_id}", response_model=BaseResponse[None])
def delete_applicant(applicant_id: str, db: Session = Depends(get_db)):
    return applicant_controller.delete_applicant(applicant_id, db)
