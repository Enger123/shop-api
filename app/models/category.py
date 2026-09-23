from app.models.base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List

class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(unique=True)
    products: Mapped[List['Product']] = relationship(back_populates='category',cascade="all, delete-orphan")

    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"

from app.models.product import Product