from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

class Cart(Base):
    __tablename__ = "carts"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    users: Mapped['User'] = relationship(back_populates='cart')
    cart_items: Mapped[list['CartItem']] = relationship(back_populates='cart')

    def __repr__(self):
        return f"<id={self.id}, user_id={self.user_id}, created_at={self.created_at}, updated_at={self.updated_at}>"

from app.models.user import User
from app.models.cart_item import CartItem
