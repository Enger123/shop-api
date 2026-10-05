from pydantic import BaseModel, Field
from typing import Literal

class UserCreateSchema(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=25)
    role: Literal["ADMIN", "USER"]

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    model_config = {'from_attributes': True}

class UserUpdateSchema(BaseModel):
    email: str | None = None
    role: Literal["ADMIN", "USER"] | None = None 
