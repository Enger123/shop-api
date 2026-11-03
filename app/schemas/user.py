from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Literal

class UserCreateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')
    email: EmailStr
    password: str = Field(min_length=6, max_length=25)

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    model_config = {'from_attributes': True}

class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')
    email: EmailStr | None = None
