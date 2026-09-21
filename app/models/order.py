from app.models.base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime   

class Order(Base):
    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(back_populates='orders')
    status: Mapped[str]
    total_price: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

from app.models import User