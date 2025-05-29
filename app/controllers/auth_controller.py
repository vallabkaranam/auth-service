from fastapi import HTTPException
from password_validator import PasswordValidator
from passlib.context import CryptContext

from app.interfaces.user_interface import UserInterface
from app.schemas.user_schemas import UserResponse


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

