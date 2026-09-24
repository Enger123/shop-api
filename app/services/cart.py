from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartSchema, CartResponse
from app.repositories.cart import CartRepository
from app.repositories.product import ProductRepository
from fastapi import HTTPException

class CartService:
    def __init__(self, db: Session):
            self.db = db
            self.cart_repository = CartRepository(db)
            self.product_repository = ProductRepository(db)

    def add_product_in_cart(
                self,
                creating_cart: CartSchema,
                current_user
                ):
        product = self.product_repository.get_product(creating_cart.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product does not exist")
        cart = self.cart_repository.get_user_cart(current_user.id)
        if cart is None:
            cart = self.cart_repository.create_cart(current_user.id)
            self.db.commit()
            self.db.refresh(cart)
        new_product_in_cart = self.cart_repository.add_product_in_cart(
             product_id=product.id,
             cart_id=cart.id,
             quantity=creating_cart.quantity
        )
        self.db.commit()
        self.db.refresh(new_product_in_cart)
        return CartResponse.model_validate(new_product_in_cart)
