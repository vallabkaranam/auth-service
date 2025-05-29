from typing import Any
from fastapi import APIRouter, Depends

from app.controllers.auth_controller import AuthController
from app.schemas.auth_schemas import SignupUserRequest


router = APIRouter()

def get_auth_controller() -> AuthController:
    return AuthController()

@router.post("/signup")
async def signup_user(
    request: SignupUserRequest,
    auth_controller: AuthController = Depends(get_auth_controller)
    )-> Any:
# SignupUserResponse:
    return auth_controller.signup_user(request)
