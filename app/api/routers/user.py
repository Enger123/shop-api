from fastapi import APIRouter
from app.api.dependencies import Current_user, UserServiceDep
from app.schemas.user import UserCreateSchema, UserUpdateSchema

router = APIRouter(tags=["users"])

@router.get("/users")
def list_users(user_service: UserServiceDep):
    return user_service.list_users()

@router.post("/users")
def create_user(new_user: UserCreateSchema,
                user_service: UserServiceDep):
    return user_service.create_user(new_user)

@router.get("/users/{user_id}")
def get_user(user_id: int, user_service: UserServiceDep):
    return user_service.get_user(user_id)

@router.patch("/users")
def change_user(current_user,
                    new_user: UserUpdateSchema,
                    user_service: UserServiceDep
                    ):
    return user_service.change_user(change_user, new_user)

@router.delete("/users")
def delete_user(current_user, user_service: UserServiceDep):
    return user_service.delete_user(current_user)
