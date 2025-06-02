from fastapi import HTTPException
from password_validator import PasswordValidator
from passlib.context import CryptContext

from app.interfaces.user_interface import UserInterface
from app.schemas.user_schemas import UserResponse
from app.utils.jwt import create_access_token, create_refresh_token


schema = PasswordValidator()
schema \
    .min(8) \
    .max(100) \
    .has().uppercase() \
    .has().lowercase() \
    .has().digits() \
    .has().no().spaces()


class AuthController:
    def __init__(self, user_interface: UserInterface):
        self.user_interface = user_interface

    def signup_user(self, user_payload):
        """
        Checks if email exists in database.
        If new user, checks password strength.
        If email and password are valid, encrypt password
        Then, create a new user with given details.
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
            first_name=new_user.first_name,
            last_name=new_user.last_name
        )
    
    def login_user(self, login_payload):
        """
        Validates credentials:
        - validates that email exists
        - validates that password matches

        Returns:
        Access Token (JWT)
        Refresh Token (JWT)
        Token expiration timestamps
        """

        attempted_email = login_payload.email

        # fetch user by user email
        user = self.user_interface.get_user_by_email(attempted_email)
        if not user:
            raise HTTPException(
                status_code=404,
                # detail="User email not found."
                detail="Email or password incorrect."
            )
        
        # validate password
        attempted_password = login_payload.password
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        is_password_matched = pwd_context.verify(attempted_password, user.hashed_password)

        if not is_password_matched:
            raise HTTPException(
                status_code=401,
                # detail="Password does not match"
                detail="Email or password incorrect."
            )
        
        token_data = {
            "sub": user.email,
            "user_id": user.id    
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

