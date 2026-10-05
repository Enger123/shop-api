from pydantic import BaseModel, Field

class ReviewCreateSchema(BaseModel):
    rating: int = Field(ge=0, le=10)
    text: str

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    order_id: int
    product_id: int
    rating: int
    text: str
    model_config={'from_attributes': True}