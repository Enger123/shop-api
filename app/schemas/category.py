from pydantic import BaseModel

class CategoryCreateSchema(BaseModel):
    name: str
    model_config = {'from_attributes': True}

class CategoryResponse(BaseModel):
    id: int
    name: str

class CategoryUpdateSchema(BaseModel):
    name: str | None = None