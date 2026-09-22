from sqlalchemy.orm import Session
from models import User
from app.core.security import hash_password
from sqlalchemy import select
from app.schemas.user import UserCreateSchema

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, new_user: UserCreateSchema):
        user = User(
            email=new_user.email,
            password_hash = hash_password(new_user.password),
            role = new_user.role
        )
        self.db.add(user)
        return user

    def get_user_byemail(self, email: str):
        return self.db.scalars(
            select(User).where(User.email==email)
        ).first()

    def list_users(self):
        return self.db.scalars(
            select(User)
        ).all()

    def get_user(self, user_id: int):
        return self.db.scalars(
            select(User).where(User.id==user_id)
        ).first()

    def delete_user(self, user):
        self.db.delete(user)
