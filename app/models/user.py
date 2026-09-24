from app.models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    email: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str]
    cart: Mapped['Cart'] = relationship(back_populates='users', cascade="all, delete-orphan")
    reviews: Mapped[list['Review']] = relationship(back_populates="user")
    orders: Mapped[list['Order']] = relationship(back_populates="user")

    def __repr__(self):
        return f"<id={self.id}, email={self.email}, password_hash={self.password_hash}, role={self.role}>"

from app.models.cart import Cart
from app.models.review import Review
from app.models.order import Order