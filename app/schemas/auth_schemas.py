from datetime import datetime
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

class LoginUserRequest(BaseModel):
    email: str = Field(..., 
                      description="The email of the user",
                      example="bob.smith@email.com")
    password: str = Field(...,
                          description="The password of the user",
                          example="Password123")
    
class TokenData(BaseModel):
    token: str = Field(...,
                       description="The token generated for the user",
                        example="SAMPLE.TOKEN"
                        )
    expiration: datetime = Field(...,
                            description="The expiration timestamp of the token",
                            example="2025-06-02T22:38:30.935254+00:00")
    
    iat: datetime = Field(...,
                     description="The issued at timestamp of the token",
                     example="2025-06-02T22:38:30.935254+00:00")

class LoginUserResponse(BaseModel):
    access_token: TokenData = Field(...,
                               description="Data about the short-lived access token generated for the user",
                              )
    
    refresh_token: TokenData = Field(...,
                                description="Data about the long-living token generated for the user to send to the refresh endpoint when access token expires",
                                )


        