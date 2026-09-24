from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Product(Base):
    __tablename__ = "products"

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    stock: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    is_active: Mapped[bool]
    category: Mapped['Category'] = relationship(back_populates='products')
    reviews: Mapped[list['Review']] = relationship(back_populates="product")
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='product')
    cart_items: Mapped[list['CartItem']] = relationship(back_populates='product')
    
    def __repr__(self):
        return f"<id={self.id}, name={self.name}, description={self.description}, price={self.price}, stock={self.stock}, category_id={self.category_id}, is_active={self.is_active}>"

from app.models.category import Category
from app.models.review import Review
from app.models.order_item import OrderItem
from app.models.cart_item import CartItem