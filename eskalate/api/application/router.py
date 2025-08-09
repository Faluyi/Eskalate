from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from eskalate.api.application.controller import application_controller
from eskalate.db.util import get_db
from eskalate.schemas.application.request import ApplicationCreate
from eskalate.schemas.application.response import ApplicationResponse
from eskalate.schemas.base import BaseResponse

router = APIRouter()

@router.post("/", response_model=BaseResponse[ApplicationResponse])
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    return application_controller.create_application(payload, db)

@router.get("/", response_model=BaseResponse[List[ApplicationResponse]])
def list_applications(db: Session = Depends(get_db)):
    return application_controller.list_applications(db)

@router.get("/{application_id}", response_model=BaseResponse[ApplicationResponse])
def get_application(application_id: str, db: Session = Depends(get_db)):
    return application_controller.get_application(application_id, db)

@router.put("/{application_id}", response_model=BaseResponse[ApplicationResponse])
def update_application(application_id: str, payload: ApplicationCreate, db: Session = Depends(get_db)):
    return application_controller.update_application(application_id, payload, db)

@router.delete("/{application_id}", response_model=BaseResponse[None])
def delete_application(application_id: str, db: Session = Depends(get_db)):
    return application_controller.delete_application(application_id, db)
