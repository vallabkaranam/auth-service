from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.controllers.auth_controller import AuthController
from app.db.get_db import get_db
from app.interfaces.user_interface import UserInterface
from app.schemas.auth_schemas import LoginUserRequest, LoginUserResponse, RefreshUserRequest, SignupUserRequest, TokenResponse
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

@router.post("/login", response_model=LoginUserResponse)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_controller: AuthController = Depends(get_auth_controller)
) -> LoginUserResponse:
    login_payload = LoginUserRequest(
        email=form_data.username,
        password=form_data.password
    )

    try:
        return auth_controller.login_user(login_payload)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to login user: {str(e)}"
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

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_controller: AuthController = Depends(get_auth_controller)
) -> TokenResponse:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    login_payload = LoginUserRequest(
        email=form_data.username,
        password=form_data.password
    )
    
    try:
        response = auth_controller.login_user(login_payload)
        return TokenResponse(
            access_token=response["access_token"]["token"],
            token_type="bearer"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get access token: {str(e)}"
        )

