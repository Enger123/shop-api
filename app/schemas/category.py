from pydantic import BaseModel

class CategoryCreateSchema(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    model_config = {'from_attributes': True}


class CategoryUpdateSchema(BaseModel):
    name: str | None = None