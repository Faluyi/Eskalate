from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from eskalate.db.models.user import User, UserRole
from eskalate.schemas.base import BaseResponse
from eskalate.schemas.company.request import CompanyCreate
from eskalate.schemas.company.response import CompanyResponse


class CompanyController:
    def create_company(payload: CompanyCreate, db: Session) -> BaseResponse[CompanyResponse]:
        company = User(
            name=payload.name,
            email=payload.email,
            website=payload.website,
            description=payload.description,
            location=payload.location
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        return BaseResponse(success=True, message="Company created", object=CompanyResponse.from_orm(company))

    def list_companies(db: Session) -> BaseResponse[List[CompanyResponse]]:
        companies = db.query(User).filter(User.role == UserRole.company).all()
        return BaseResponse(success=True, message="Companies fetched", object=[CompanyResponse.from_orm(c) for c in companies])

    def get_company(company_id: str, db: Session) -> BaseResponse[CompanyResponse]:
        company = db.query(User).filter(User.id == company_id, User.role == UserRole.company).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return BaseResponse(success=True, message="Company fetched", object=CompanyResponse.from_orm(company))

    def update_company(company_id: str, payload: CompanyCreate, db: Session) -> BaseResponse[CompanyResponse]:
        company = db.query(User).filter(User.id == company_id, User.role == UserRole.company).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        company.name = payload.name
        company.email = payload.email
        company.website = payload.website
        company.description = payload.description
        company.location = payload.location
        db.commit()
        db.refresh(company)

        return BaseResponse(success=True, message="Company updated", object=CompanyResponse.from_orm(company))

    def delete_company(company_id: str, db: Session) -> BaseResponse[None]:
        company = db.query(User).filter(User.id == company_id, User.role == UserRole.company).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        db.delete(company)
        db.commit()
        return BaseResponse(success=True, message="Company deleted", object=None)


company_controller = CompanyController()