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

from app.models.user import User