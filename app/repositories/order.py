from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.order import Order
from datetime import datetime

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_my_orders(self, user_id: int):
        return self.db.scalars(
            select(Order).where(Order.user_id==user_id)
        ).all()
    
    def get_my_order(self, user_id: int, order_id: int):
        return self.db.scalars(
                    select(Order)
                    .where(
                        Order.user_id==user_id,
                        Order.id==order_id
                        )
                ).first()

    def add_product_to_orders(self, product_price, user_id: int):
        new_order = Order(
            user_id=user_id,
            status=...,
            total_price=product_price.price,
            created_at=datetime.now()
        )
        self.db.add(new_order)
        return new_order
        
        