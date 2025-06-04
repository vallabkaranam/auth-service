import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.interfaces.user_interface import UserInterface
from app.schemas.user_schemas import UserResponse
from jose import jwt

load_dotenv()

# JWT configuration for token validation
ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# OAuth2 scheme for token extraction from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> UserResponse:
    """
    FastAPI dependency that validates JWT access tokens and returns the authenticated user.
    
    Process:
    1. Extracts JWT from Authorization header
    2. Decodes and validates token signature
    3. Verifies user exists and matches token claims
    
    Args:
        token: JWT access token from Authorization header
        db: Database session
        
    Returns:
        UserResponse: Authenticated user data
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
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
        role=user.role,
        first_name=user.first_name,
        last_name=user.last_name
    )

def check_admin_role(
        current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    FastAPI dependency that enforces admin-only access to protected routes.
    
    Args:
        current_user: Authenticated user from get_current_user dependency
        
    Returns:
        UserResponse: User data if admin role is verified
        
    Raises:
        HTTPException: If user is not an admin
    """
    try:
        role = current_user.role
        
        if role != "ADMIN":
            raise HTTPException(
            status_code=403,
            detail="Unauthorized request, you must be an admin"
        )

        return current_user
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized request"
        )

        