from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.user_controller import UserController
from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.interfaces.user_interface import UserInterface
from app.schemas.user_schemas import UserResponse


router = APIRouter()

def get_user_controller(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
        ) -> UserController:
    user_interface = UserInterface(db)
    return UserController(user_interface, current_user)

@router.get("/me", response_model=UserResponse)
async def get_current_user(user_controller: UserController = Depends(get_user_controller)) -> UserResponse:
    try:
        return user_controller.get_current_user()
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get current user: {str(e)}"
        )