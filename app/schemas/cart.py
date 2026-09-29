from pydantic import BaseModel, Field

class ProductInfo(BaseModel):
    id: int
    name: str
    summary_price: int
    model_config = {'from_attributes': True}


class CartSchema(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class CartResponse(BaseModel):
    id: int
    cart_id: int
    product: ProductInfo
    model_config={'from_attributes': True}