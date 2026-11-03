from fastapi import APIRouter
from app.api.dependencies import Current_user, UserServiceDep
from app.schemas.user import UserCreateSchema, UserUpdateSchema, UserResponse

router = APIRouter(tags=["Users"])

@router.get("/users", response_model=list[UserResponse])
def list_users(user_service: UserServiceDep) -> list[UserResponse]:
    return user_service.list_users()

@router.post("/users", response_model=UserResponse)
def create_user(new_user: UserCreateSchema,
                user_service: UserServiceDep) -> UserResponse:
    return user_service.create_user(new_user)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, user_service: UserServiceDep) -> UserResponse:
    return user_service.get_user(user_id)

@router.patch("/users", response_model=UserResponse)
def change_user(current_user: Current_user,
                    new_user: UserUpdateSchema,
                    user_service: UserServiceDep
                    ) -> UserResponse:
    return user_service.change_user(current_user, new_user)

@router.delete("/users")
def delete_user(current_user: Current_user, user_service: UserServiceDep):
    return user_service.delete_user(current_user)
