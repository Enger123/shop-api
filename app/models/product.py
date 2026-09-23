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
    category: Mapped['Category'] = relationship(back_populates='products')
    is_active: Mapped[bool]

    def __repr__(self):
        return f"<name={self.name}, description={self.description}, price={self.price}, stock={self.stock}, category_id={self.category_id}, is_active={self.is_active}>"

from app.models.category import Category