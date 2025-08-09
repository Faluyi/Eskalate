from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.user import UserCreate, LoginRequest, UserResponse
from app.schemas.base import BaseResponse
from app.controllers import auth_controller

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=BaseResponse[UserResponse])
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    return auth_controller.signup(payload, db)

@router.get("/verify-email", response_model=BaseResponse[None])
def verify_email(token: str, db: Session = Depends(get_db)):
    return auth_controller.verify_email(token, db)

@router.post("/login", response_model=BaseResponse[str])
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return auth_controller.login(payload, db)
