from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class CartItem(Base):
    __tablename__ = "cart_items"

    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))
    cart: Mapped['Cart'] = relationship(back_populates='cart_items')

from app.models import Cart