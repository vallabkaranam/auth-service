from pydantic import BaseModel, Field


class SignupUserRequest(BaseModel):
    first_name: str = Field(..., 
                            description="The first name of the user", 
                            example="Bob")
    last_name: str = Field(...,
                           description="The last name of the user",
                           example="Smith")
    email: str = Field(...,
                       description="The email of the user",
                       example="bob.smith@email.com")
    password: str = Field(...,
                          description="The password of the user",
                          example="Password123")
    
class SignupUserResponse(BaseModel):
    first_name: str = Field(..., 
                            description="The first name of the created user", 
                            example="Bob")
    last_name: str = Field(...,
                           description="The last name of the created user",
                           example="Smith")
    email: str = Field(...,
                       description="The email of the created user",
                       example="bob.smith@email.com")
    # created_at: 
    # updated_at:

        