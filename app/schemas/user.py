from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    model_config = {'from_attributes': True}

class UserUpdateSchema(BaseModel):
    email: str | None = None
    role: str | None = None 
