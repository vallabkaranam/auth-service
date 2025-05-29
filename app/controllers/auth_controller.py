
from fastapi import HTTPException
from password_validator import PasswordValidator
from passlib.context import CryptContext


schema = PasswordValidator()
schema \
    .min(8) \
    .max(100) \
    .has().uppercase() \
    .has().lowercase() \
    .has().digits() \
    .has().no().spaces()


class AuthController:
    # def __init__(self):
    #     self

    def signup_user(self, user_payload):
        """
        Checks if email exists in database.
        If new user, checks password strength.
        If email and password are valid, encrypt password
        Then, create a new user with given details.
        """

        # check if email exists in database.

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
        
        return pwd_context.verify(plain_text_password, hashed_password)

