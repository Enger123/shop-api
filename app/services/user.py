from sqlalchemy.orm import Session
from app.schemas.user import UserCreateSchema
from app.repositories.user import UserRepository
from fastapi import HTTPException

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def create_user(self,
        create_user: UserCreateSchema,
        ):
        user = self.user_repository.get_user(create_user.email)
        if user:
            raise HTTPException(
                status_code=403, detail='User already exists'
            )

    