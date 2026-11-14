from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartSchema, CartResponse, ProductInfo
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
        
          if product.stock < creating_cart.quantity:
               raise HTTPException(status_code=409, detail='Product not enough')
        
          cart = self.cart_repository.get_user_cart(current_user.id)
          if cart is None:
               cart = self.cart_repository.create_cart(current_user.id)
               self.db.flush()

          # додав щоб не можна було з тим самим id додати продукт, лише оновити кількість
          # можна в іншому роуті
          product_in_cart = self.cart_repository.get_product_in_cart(
               user_id=current_user.id,
               product_id=product.id
          )
          if product_in_cart is not None:
               if product.id == product_in_cart.product_id:
                    raise HTTPException(status_code=409, detail='Product already in cart')
          ## по сюди
          new_product_in_cart = self.cart_repository.add_product_in_cart(
               product_id=product.id,
               cart_id=cart.id,
               quantity=creating_cart.quantity
          )
          self.db.commit()
          self.db.refresh(new_product_in_cart)

          return CartResponse(
               id=new_product_in_cart.id,
               cart_id=new_product_in_cart.cart_id,
               product=ProductInfo(
                    id=new_product_in_cart.product_id,
                    name=new_product_in_cart.product.name,
                    product_amount=new_product_in_cart.quantity,
                    summary_price=new_product_in_cart.product.price*creating_cart.quantity
               )
          )

     def change_cart_product_quantity(self, updating_cart: CartSchema, current_user):
          product = self.product_repository.get_product(updating_cart.product_id)
          if not product:
               raise HTTPException(status_code=404, detail="Product does not exist")
          
          if product.stock < updating_cart.quantity:
               raise HTTPException(status_code=409, detail='Product not enough')

          product_to_change = self.cart_repository.get_product_in_cart(
               current_user.id,
               product_id=updating_cart.product_id
               )
          
          product_to_change.quantity = updating_cart.quantity
          self.db.commit()
          self.db.refresh(product_to_change)

          return CartResponse(
               id=product_to_change.id,
               cart_id=product_to_change.cart_id,
               product=ProductInfo(
                    id=product_to_change.product_id,
                    name=product_to_change.product.name,
                    product_amount=product_to_change.quantity,
                    summary_price=product_to_change.quantity*product_to_change.product.price
               )
          )

     def delete_product_from_cart(self, product_id, current_user: int):
          product_in_cart = self.cart_repository.get_product_in_cart(
               current_user.id,
               product_id
          )
          if not product_in_cart:
               raise HTTPException(status_code=404, detail='Product is not in the cart')

          self.cart_repository.delete_product_from_cart(product_in_cart)
          self.db.commit()

     def get_products_in_my_cart(
              self, 
              current_user,

        ):
          cart_items = self.cart_repository.get_products_in_cart(current_user.id)
          return [CartResponse(
                         id=cart_item.id,
                         cart_id=cart_item.cart_id,
                         product=ProductInfo(
                              id=cart_item.product_id,
                              name=cart_item.product.name,
                              product_amount=cart_item.quantity,
                              summary_price=cart_item.quantity*cart_item.product.price
                         )
                    ) for cart_item in cart_items
          ]
