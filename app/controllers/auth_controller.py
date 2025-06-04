from datetime import datetime, timezone
from fastapi import HTTPException
from password_validator import PasswordValidator
from passlib.context import CryptContext

from app.interfaces.user_interface import UserInterface
from app.schemas.user_schemas import UserResponse
from app.utils.jwt import create_access_token, create_refresh_token, decode_refresh_token

# Password validation schema
schema = PasswordValidator()
schema \
    .min(8) \
    .max(100) \
    .has().uppercase() \
    .has().lowercase() \
    .has().digits() \
    .has().no().spaces()

class AuthController:
    """
    Controller handling user authentication operations including signup, login, and token refresh.
    Implements security best practices for password handling and JWT token management.
    """
    def __init__(self, user_interface: UserInterface):
        self.user_interface = user_interface

    def signup_user(self, user_payload):
        """
        Handles new user registration with security validations.
        
        Performs the following checks:
        1. Verifies email is not already registered
        2. Validates password meets complexity requirements
        3. Securely hashes password before storage
        
        Args:
            user_payload: User registration data including email, password, and personal info
            
        Returns:
            UserResponse: Created user data (excluding sensitive information)
            
        Raises:
            HTTPException: If email exists or password doesn't meet requirements
        """
        # check if email exists in database.
        user_with_email = self.user_interface.get_user_by_email(user_payload.email)
        if (user_with_email):
            raise HTTPException(status_code=400, detail="Email already registered, log in instead")

        # check strength of password
        plain_text_password = user_payload.password

        password_is_valid = schema.validate(plain_text_password)
        
        if not password_is_valid:
            raise HTTPException(status_code=400, 
                                detail="Password does not meet complexity requirements. "
                       "It must have at least 8 characters, include uppercase, lowercase, digits, "
                       "and must not contain spaces.")
        
        # encrypt password
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(plain_text_password)
        
        # Create new user
        new_user = self.user_interface.create_user(
            email=user_payload.email,
            hashed_password=hashed_password,
            first_name=user_payload.first_name,
            last_name=user_payload.last_name
        )
        
        # Convert to Pydantic model for response
        return UserResponse(
            id=new_user.id,
            email=new_user.email,
            role=new_user.role,
            first_name=new_user.first_name,
            last_name=new_user.last_name
        )
    
    def login_user(self, login_payload):
        """
        Authenticates user credentials and issues JWT tokens.
        
        Process:
        1. Validates user exists
        2. Verifies password matches stored hash
        3. Generates access and refresh tokens
        
        Args:
            login_payload: User login credentials (email and password)
            
        Returns:
            dict: Access and refresh tokens with their expiration timestamps
            
        Raises:
            HTTPException: If credentials are invalid
        """
        attempted_email = login_payload.email

        # fetch user by user email
        user = self.user_interface.get_user_by_email(attempted_email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Email or password incorrect."
            )
        
        # validate password
        attempted_password = login_payload.password
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        is_password_matched = pwd_context.verify(attempted_password, user.hashed_password)

        if not is_password_matched:
            raise HTTPException(
                status_code=401,
                detail="Email or password incorrect."
            )
        
        token_data = {
            "sub": user.email,
            "user_id": user.id,
            "role": user.role    
            }
        access_token, access_token_exp, access_token_iat = create_access_token(token_data)
        refresh_token, refresh_token_exp, refresh_token_iat = create_refresh_token(token_data)

        return {
            "access_token": {
                "token": access_token,
                "expiration": access_token_exp,
                "iat": access_token_iat
                },
            "refresh_token": {
                "token": refresh_token,
                "expiration": refresh_token_exp,
                "iat": refresh_token_iat
            }
        }
    
    def refresh_user(self, refresh_payload):
        """
        Issues new access and refresh tokens using a valid refresh token.
        
        Process:
        1. Validates refresh token hasn't expired
        2. Verifies user still exists and matches token
        3. Issues new token pair
        
        Args:
            refresh_payload: Current refresh token
            
        Returns:
            dict: New access and refresh tokens with expiration timestamps
            
        Raises:
            HTTPException: If refresh token is invalid or expired
        """
        payload = decode_refresh_token(refresh_payload.refresh_token)
        now = datetime.now(timezone.utc)
        exp_timestamp = payload.get("exp")  # This is an int
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)        
    
        # check that the refresh token is active
        if (now > exp_datetime):
            raise HTTPException(
                status_code=401,
                detail="Refresh token has expired"
            )
        
        # check if user is valid
        user = self.user_interface.get_user_by_email(payload.get("sub"))
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Cannot find user"
            )
        
        if user.id != payload.get("user_id"):
            raise HTTPException(
                status_code=401,
                detail="User does not match"
            )
        
        token_data = {
            "sub": payload.get("sub"),
            "user_id": payload.get("user_id"),
            "role": payload.get("role")
        }

        access_token, access_token_exp, access_token_iat = create_access_token(token_data)
        refresh_token, refresh_token_exp, refresh_token_iat = create_refresh_token(token_data)

        return {
            "access_token": {
                "token": access_token,
                "expiration": access_token_exp,
                "iat": access_token_iat
                },
            "refresh_token": {
                "token": refresh_token,
                "expiration": refresh_token_exp,
                "iat": refresh_token_iat
            }
        }

        



