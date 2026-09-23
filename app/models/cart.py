from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

class Cart(Base):
    __tablename__ = "carts"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    users: Mapped[list['User']] = relationship(back_populates='cart')
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

from app.models.user import User
