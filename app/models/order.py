from app.models.base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime   

class Order(Base):
    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[str]
    total_price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    user: Mapped['User'] = relationship(back_populates='orders')
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='order', cascade="all, delete-orphan")
    reviews: Mapped[list['Review']] = relationship(back_populates="order")

    def __repr__(self):
        return f"<id={self.id}, user_id={self.user_id}, status={self.status}, total_price={self.total_price}, created_at={self.created_at}>"

from app.models.user import User
from app.models.order_item import OrderItem
from app.models.review import Review