from sqlalchemy.orm import Session
from app.repositories.order import OrderRepository
from app.schemas.order import OrderResponse
from fastapi import HTTPException


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repository = OrderRepository(db)

    def get_my_orders(self, current_user):
        user_orders = self.order_repository.get_my_orders(current_user.id)
        return [OrderResponse.model_validate(order)
                 for order in user_orders]
        
    def get_my_order(self, current_user, order_id: int):
        user_order = self.order_repository.get_my_order(current_user.id, order_id)
        if not user_order:
            raise HTTPException(status_code=404, detail='Orders not found')
        return [OrderResponse.model_validate(order)
            for order in user_order]

    def add_product_to_orders(self, product_price, current_user):
        new_order = self.order_repository.add_product_to_orders(
            product_price, current_user.id
            )
        self.db.commit()
        self.db.refresh(new_order)
        return OrderResponse.model_validate(new_order)

