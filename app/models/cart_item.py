from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class CartItem(Base):
    __tablename__ = "cart_items"

    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int]
    cart: Mapped['Cart'] = relationship(back_populates='cart_items')
    product: Mapped['Product'] = relationship(back_populates='cart_items')

    def __repr__(self):
        return f"<id={self.id}, cart_id={self.cart_id}, product_id={self.product_id}>"

from app.models.cart import Cart
from app.models.product import Product