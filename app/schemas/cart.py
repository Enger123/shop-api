from pydantic import BaseModel

class ProductInfo(BaseModel):
    id: int
    name: str
    price: int
    model_config = {'from_attributes': True}


class CartSchema(BaseModel):
    product_id: int
    quantity: int

class CartResponse(BaseModel):
    id: int
    cart_id: int
    product: ProductInfo
    model_config={'from_attributes': True}