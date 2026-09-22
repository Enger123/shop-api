from app.models.base import Base
from sqlalchemy.orm import Mapped

class User(Base):
    __tablename__ = "users"

    email: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str]

    def __repr__(self):
        return f"<id={self.id}, email={self.email}, password_hash={self.password_hash}, role={self.role}>"