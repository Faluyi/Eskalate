from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from eskalate.db.util import get_db
from eskalate.schemas.base import BaseResponse
from eskalate.schemas.company.request import CompanyCreate
from eskalate.schemas.company.response import CompanyResponse
from eskalate.api.company.controller import company_controller
 
router = APIRouter()

@router.post("/", response_model=BaseResponse[CompanyResponse])
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    return company_controller.create_company(payload, db)

@router.get("/", response_model=BaseResponse[List[CompanyResponse]])
def list_companies(db: Session = Depends(get_db)):
    return company_controller.list_companies(db)

@router.get("/{company_id}", response_model=BaseResponse[CompanyResponse])
def get_company(company_id: str, db: Session = Depends(get_db)):
    return company_controller.get_company(company_id, db)

@router.put("/{company_id}", response_model=BaseResponse[CompanyResponse])
def update_company(company_id: str, payload: CompanyCreate, db: Session = Depends(get_db)):
    return company_controller.update_company(company_id, payload, db)

@router.delete("/{company_id}", response_model=BaseResponse[None])
def delete_company(company_id: str, db: Session = Depends(get_db)):
    return company_controller.delete_company(company_id, db)
