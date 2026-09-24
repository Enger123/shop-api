from pydantic import BaseModel
from datetime import datetime

class OrderResponse(BaseModel):
    id: int
    total_price: int
    status: str
    user_id: int
    created_at: datetime
    model_config = {'from_attributes': True}
