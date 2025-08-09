from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from eskalate.db.models.user import User, UserRole
from eskalate.schemas.applicant.request import ApplicantCreate
from eskalate.schemas.applicant.response import ApplicantResponse
from eskalate.schemas.base import BaseResponse
from eskalate.utils.auth_util import hash_password


class ApplicantController:
    def create_applicant(self, payload: ApplicantCreate, db: Session) -> BaseResponse[ApplicantResponse]:
        applicant = User(
            name=payload.name,
            email=payload.email,
            password=hash_password(payload.password),
            role=UserRole.applicant
        )
        db.add(applicant)
        db.commit()
        db.refresh(applicant)
        return BaseResponse(success=True, message="Applicant created", object=ApplicantResponse.model_validate(applicant))

    def list_applicants(self, db: Session) -> BaseResponse[List[ApplicantResponse]]:
        applicants = db.query(User).filter(User.role == UserRole.applicant).all()
        return BaseResponse(success=True, message="Applicants fetched", object=[ApplicantResponse.model_validate(a) for a in applicants])

    def get_applicant(self, applicant_id: str, db: Session) -> BaseResponse[ApplicantResponse]:
        applicant = db.query(User).filter(User.role == UserRole.applicant, User.id == applicant_id).first()
        if not applicant:
            raise HTTPException(status_code=404, detail="Applicant not found")
        return BaseResponse(success=True, message="Applicant fetched", object=ApplicantResponse.model_validate(applicant))

    def update_applicant(self, applicant_id: str, payload: ApplicantCreate, db: Session) -> BaseResponse[ApplicantResponse]:
        applicant = db.query(User).filter(User.role == UserRole.applicant, User.id == applicant_id).first()
        if not applicant:
            raise HTTPException(status_code=404, detail="Applicant not found")

        applicant.name = payload.name
        applicant.email = payload.email
        db.commit()
        db.refresh(applicant)

        return BaseResponse(success=True, message="Applicant updated", object=ApplicantResponse.model_validate(applicant))

    def delete_applicant(self, applicant_id: str, db: Session) -> BaseResponse[None]:
        applicant = db.query(User).filter(User.id == applicant_id).first()
        if not applicant:
            raise HTTPException(status_code=404, detail="Applicant not found")

        db.delete(applicant)
        db.commit()
        return BaseResponse(success=True, message="Applicant deleted", object=None)
    

applicant_controller = ApplicantController()
