from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from eskalate.db.util import get_db
from eskalate.schemas.auth.request import LoginRequest, UserCreate
from eskalate.schemas.auth.response import UserResponse
from eskalate.schemas.base import BaseResponse
from eskalate.api.auth.controller import auth_controller

router = APIRouter()

@router.post("/signup", response_model=BaseResponse[UserResponse])
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    return auth_controller.signup(payload, db)

@router.get("/verify-email", response_model=BaseResponse[None])
def verify_email(token: str, db: Session = Depends(get_db)):
    return auth_controller.verify_email(token, db)

@router.post("/login", response_model=BaseResponse[str])
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return auth_controller.login(payload, db)
