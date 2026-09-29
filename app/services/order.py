from sqlalchemy.orm import Session
from app.repositories.order import OrderRepository
from app.repositories.cart import CartRepository
from app.schemas.order import OrderResponse
from fastapi import HTTPException


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repository = OrderRepository(db)
        self.cart_repository = CartRepository(db)

    def get_my_orders(self, current_user):
        user_orders = self.order_repository.get_my_orders(current_user.id)
        return [OrderResponse.model_validate(order)
                 for order in user_orders]
        
    def get_my_order(self, current_user, order_id: int):
        user_order = self.order_repository.get_my_order(current_user.id, order_id)
        if not user_order:
            raise HTTPException(status_code=404, detail='Orders not found')
        return OrderResponse.model_validate(user_order)

    def add_to_orders(self, current_user):
        cart = self.cart_repository.get_user_cart(current_user.id)
        if cart is None:
            raise HTTPException(status_code=404, detail='Cart not found')
        
        cart_items = self.cart_repository.get_products_in_cart(current_user.id)
        if not cart_items:
            raise HTTPException(status_code=404, detail='Products not found in cart')
        
        total_price = 0
        for cart_item in cart_items:
            if cart_item.product.stock < cart_item.quantity:
                raise HTTPException(
                    status_code=409,
                    detail=f"Not enough stock for {cart_item.product.name}"
                )
            total_price += cart_item.product.price * cart_item.quantity

        general_order = self.order_repository.create_order(current_user.id, total_price)
        self.db.flush()

        self.order_repository.create_order_item(general_order.id, cart_items)

        
        self.cart_repository.clear_cart_items(cart_items)

        self.db.commit()
        self.db.refresh(general_order)

        return OrderResponse.model_validate(general_order)

