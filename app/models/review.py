from app.models.base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

class Review(Base):
    __tablename__ = "reviews"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    rating: Mapped[int]
    text: Mapped[str]
    user: Mapped['User'] = relationship(back_populates='reviews')
    product: Mapped['Product'] = relationship(back_populates="reviews")
    order: Mapped['Order'] = relationship(back_populates="reviews")

    def __repr__(self):
        return f"<id={self.id}, user_id={self.user_id}, order_id={self.order_id}, product_id={self.product_id}, rating={self.rating}, text={self.text}>"

from app.models.user import User
from app.models.product import Product
from app.models.order import Order