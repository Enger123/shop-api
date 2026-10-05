from sqlalchemy.orm import Session
from app.schemas.user import UserCreateSchema, UserResponse, UserUpdateSchema
from app.repositories.user import UserRepository
from fastapi import HTTPException

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def list_users(self):
        users = self.user_repository.list_users()
        return [
            UserResponse(
                id=user.id,
                email=user.email,
                role=user.role
                )
            for user in users
        ]

    def create_user(self,
        new_user: UserCreateSchema,
        ):
        user = self.user_repository.get_user_byemail(new_user.email)
        if user:
            raise HTTPException(
                status_code=403, detail='User already exists'
            )
        created_user = self.user_repository.create_user(new_user)
        self.db.commit()
        self.db.refresh(created_user)
        return UserResponse.model_validate(created_user)

    def get_user(self, user_id: int):
        user = self.user_repository.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return UserResponse.model_validate(user)

    def change_user(self, 
                    current_user,
                    new_user: UserUpdateSchema
                    ):
        user = self.user_repository.get_user(current_user.id)
        user_by_email = self.user_repository.get_user_byemail(new_user.email)
        if user_by_email is not None:
            raise HTTPException(status_code=403, detail='User exists')
        if new_user.email is not None:
            user.email = new_user.email
        if new_user.role is not None:
            user.role = new_user.role
        self.db.commit()
        self.db.refresh(user)
        return UserResponse.model_validate(user)

    def delete_user(self, current_user):
        user_to_del = self.user_repository.get_user(current_user.id)
        self.user_repository.delete_user(user_to_del)
        self.db.commit()
        return {'message': 'User deleted'}

        