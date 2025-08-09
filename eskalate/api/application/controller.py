from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from eskalate.db.models.application import Application
from eskalate.db.models.job import Job
from eskalate.db.models.user import User, UserRole
from eskalate.schemas.application.request import ApplicationCreate
from eskalate.schemas.application.response import ApplicationResponse
from eskalate.schemas.base import BaseResponse
import uuid
from datetime import datetime

from eskalate.services.cloudinary.service import upload_file, upload_file_bytes

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from sqlalchemy.exc import SQLAlchemyError


class ApplicationController:
    def create_application(
        payload: ApplicationCreate,
        db: Session,
        file: UploadFile = None
    ) -> BaseResponse[ApplicationResponse]:
        # Ensure applicant exists
        applicant = db.query(User).filter(
            User.role == UserRole.applicant,
            User.id == payload.applicant_id
        ).first()
        if not applicant:
            raise HTTPException(status_code=404, detail="Applicant not found")

        # Ensure job exists
        job = db.query(Job).filter(Job.id == payload.job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        file_url = None
        if file:
            try:
                file_bytes = file.file.read()
                upload_result = upload_file_bytes(
                    file_bytes,
                    filename=file.filename,
                    folder="applications",
                    resource_type="auto"
                )
                file_url = upload_result["secure_url"]
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

        try:
            application = Application(
                id=str(uuid.uuid4()),
                applicant_id=payload.applicant_id,
                job_id=payload.job_id,
                status=payload.status or "pending",
                cover_letter=payload.cover_letter,
                attachment_url=file_url,
                created_at=datetime.utcnow()
            )
            db.add(application)
            db.commit()
            db.refresh(application)

            return BaseResponse(
                success=True,
                message="Application created",
                object=ApplicationResponse.model_validate(application)  # for Pydantic v2
            )

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    def list_applications(db: Session) -> BaseResponse[List[ApplicationResponse]]:
        applications = db.query(Application).all()
        return BaseResponse(success=True, message="Applications fetched", object=[ApplicationResponse.from_orm(a) for a in applications])

    def get_application(application_id: str, db: Session) -> BaseResponse[ApplicationResponse]:
        application = db.query(Application).filter(Application.id == application_id).first()
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        return BaseResponse(success=True, message="Application fetched", object=ApplicationResponse.from_orm(application))

    def update_application(application_id: str, payload: ApplicationCreate, db: Session) -> BaseResponse[ApplicationResponse]:
        application = db.query(Application).filter(Application.id == application_id).first()
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        application.status = payload.status
        application.cover_letter = payload.cover_letter
        db.commit()
        db.refresh(application)

        return BaseResponse(success=True, message="Application updated", object=ApplicationResponse.from_orm(application))

    def delete_application(application_id: str, db: Session) -> BaseResponse[None]:
        application = db.query(Application).filter(Application.id == application_id).first()
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        db.delete(application)
        db.commit()
        return BaseResponse(success=True, message="Application deleted", object=None)
    
    
application_controller = ApplicationController()

