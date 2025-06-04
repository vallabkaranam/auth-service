from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int = Field(..., description="The unique identifier of the user")
    email: str = Field(..., description="The email of the user")
    role: str = Field(..., description="The role of the user")
    first_name: str = Field(..., description="The first name of the user")
    last_name: str = Field(..., description="The last name of the user")