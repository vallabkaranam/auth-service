from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.auth_controller import AuthController
from app.db.get_db import get_db
from app.interfaces.user_interface import UserInterface
from app.schemas.auth_schemas import SignupUserRequest
from app.schemas.user_schemas import UserResponse


router = APIRouter()

def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    user_interface = UserInterface(db)
    return AuthController(user_interface)

@router.post("/signup")
async def signup_user(
    request: SignupUserRequest,
    auth_controller: AuthController = Depends(get_auth_controller)
    )-> UserResponse:
    return auth_controller.signup_user(request)
