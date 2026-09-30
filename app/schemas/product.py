from pydantic import BaseModel, Field

class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: int
    stock: int = Field(gt=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    stock: int
    category_id: int
    is_active: bool
    model_config = {'from_attributes': True}

class ProductUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    stock: int | None = None
    is_active: bool | None = None