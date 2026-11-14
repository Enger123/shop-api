from sqlalchemy.orm import Session
from app.schemas.user import UserCreateSchema, UserResponse, UserUpdateSchema
from app.repositories.user import UserRepository
from fastapi import HTTPException

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_current_admin(self, current_user, operation: str):
        if current_user.role != 'ADMIN':
            raise HTTPException(status_code=403, detail=f"User can't {operation} users")
    
    def list_users(self, current_user):
        self.get_current_admin(current_user=current_user, operation='view')
        users = self.user_repository.list_users()
        return [UserResponse.model_validate(user) for user in users]

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

    def get_user(self, user_id: int, current_user):
        self.get_current_admin(current_user=current_user, operation='view')
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
        self.db.commit()
        self.db.refresh(user)
        return UserResponse.model_validate(user)

    def delete_user(self, current_user):
        user_to_del = self.user_repository.get_user(current_user.id)
        self.user_repository.delete_user(user_to_del)
        self.db.commit()
        return {'message': 'User deleted'}

        