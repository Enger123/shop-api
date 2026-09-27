from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.order import Order
from app.models.order_item import OrderItem
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

    def create_order(self, user_id: int, total_price: int):
        new_order = Order(
            user_id=user_id,
            status='pending',
            total_price=total_price,
            created_at=datetime.now()
        )
        self.db.add(new_order)
        return new_order

    def create_order_item(self, order_id: int, cart_items):
        new_order_items = [OrderItem(
            order_id=order_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        ) for cart_item in cart_items]
        self.db.add_all(new_order_items)
        return new_order_items
        