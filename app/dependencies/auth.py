import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.get_db import get_db
from app.interfaces.user_interface import UserInterface
from app.schemas.user_schemas import UserResponse
from app.utils import jwt

load_dotenv()

ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> UserResponse:
    
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
        headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if not email or not user_id:
            raise credentials_exception

        
    except Exception:
        raise credentials_exception
    
    user_interface = UserInterface(db)
    user = user_interface.get_user_by_email(email)

    if not user or user.id != user_id:
        raise credentials_exception
    
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
    )
    