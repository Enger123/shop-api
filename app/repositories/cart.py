from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.cart import Cart, CartItem
from datetime import datetime

class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_products_in_cart(self, user_id: int):
        return self.db.scalars(
            select(CartItem).join(Cart).
            where(Cart.user_id==user_id)
        ).all()

    def add_product_in_cart(
        self, 
        product_id: int, 
        cart_id: int, 
        quantity: int
    ):
        
        new_item_in_cart = CartItem(
        cart_id=cart_id,
        product_id=product_id,
        quantity=quantity
        )
        self.db.add(new_item_in_cart)
        return new_item_in_cart

    def get_user_cart(self, user_id: int):

        return self.db.scalars(select(Cart).where(Cart.user_id==user_id)
                        ).first()

    def create_cart(self, user_id: int):
        new_cart = Cart(
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.db.add(new_cart)
        return new_cart

    def clear_cart_items(self, cart_items):
        for obj in cart_items:
            self.db.delete(obj)