from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.auth_controller import AuthController
from app.db.get_db import get_db
from app.interfaces.user_interface import UserInterface
from app.schemas.auth_schemas import LoginUserRequest, LoginUserResponse, RefreshUserRequest, SignupUserRequest
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
    try: 
        return auth_controller.signup_user(request)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to signup user: {str(e)}"
        )

@router.post("/login")
async def login_user(
    request: LoginUserRequest,
    auth_controller: AuthController = Depends(get_auth_controller)
) -> LoginUserResponse:
    try:
        return auth_controller.login_user(request)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to signup user: {str(e)}"
        )

@router.post("/refresh")
async def refresh_user(
    request: RefreshUserRequest,
    auth_controller: AuthController = Depends(get_auth_controller)
) -> LoginUserResponse:

    try: 
        return auth_controller.refresh_user(request)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refresh tokens: {str(e)}"
        )

