from app.models.base import Base
from sqlalchemy.orm import Mapped

class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str]