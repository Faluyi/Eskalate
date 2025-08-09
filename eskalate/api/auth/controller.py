from fastapi import HTTPException
from sqlalchemy.orm import Session
from eskalate.db.models.user import User
from eskalate.schemas.auth.request import LoginRequest, UserCreate
from eskalate.schemas.auth.response import UserResponse
from eskalate.schemas.base import BaseResponse
from eskalate.utils.auth_util import (
    create_access_token,
    hash_password,
    verify_password,
    decode_token
)
from eskalate.services.email.service import email_service


class AuthController:
    def signup(payload: UserCreate, db: Session) -> BaseResponse[UserResponse]:
        existing_user = db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pw = hash_password(payload.password)
        user = User(
            name=payload.name,
            email=payload.email,
            password=hashed_pw,
            role=payload.role,
            is_verified=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token({"sub": str(user.id)}, expires_minutes=60)
        email_service.send_verification_email(user.email, token)

        return BaseResponse(
            success=True,
            message="User registered. Please verify email.",
            object=UserResponse.from_orm(user),
            errors=None
        )

    def verify_email(token: str, db: Session) -> BaseResponse[None]:
        payload = decode_token(token)
        user = db.query(User).filter(User.id == payload.get("sub")).first()

        if not user:
            return BaseResponse(success=False, message="Invalid token", object=None, errors=None)

        if user.is_verified:
            return BaseResponse(success=True, message="Email already verified", object=None, errors=None)

        user.is_verified = True
        db.commit()
        return BaseResponse(success=True, message="Email verified successfully", object=None, errors=None)

    def login(payload: LoginRequest, db: Session) -> BaseResponse[str]:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user or not verify_password(payload.password, user.password):
            return BaseResponse(success=False, message="Invalid credentials", object=None, errors=None)

        access_token = create_access_token({"sub": str(user.id), "role": user.role})
        return BaseResponse(success=True, message="Login successful", object=access_token, errors=None)
    
auth_controller = AuthController()
