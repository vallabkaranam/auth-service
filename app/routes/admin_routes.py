from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.admin_controller import AdminController
from app.db.session import get_db
from app.dependencies.auth import check_admin_role
from app.interfaces.user_interface import UserInterface
from app.schemas.user_schemas import UserResponse


router = APIRouter()

def get_admin_controller(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(check_admin_role)
) -> AdminController:
    user_interface = UserInterface(db)
    return AdminController(user_interface, current_user)

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(admin_controller: AdminController = Depends(get_admin_controller)):
    try:
        users = admin_controller.get_all_users()
        return users
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Cannot get all users"
        )
        

    

    