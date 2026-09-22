from app.models.base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

class Review(Base):
    __tablename__ = "reviews"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    order_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    user: Mapped['User'] = relationship(back_populates='reviews')
    rating: Mapped[int]
    text: Mapped[str]

    def __repr__(self):
            return f"<user_id={self.user_id}, order_id={self.order_id}, product_id={self.product_id}, rating={self.rating}, text={self.text}>"

from app.models.user import User