from app.models.base import Base
from sqlalchemy.orm import Mapped

class User(Base):
    __tablename__ = "users"

    email: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str]