from app.api.dependencies import CategoryServiceDep, Current_user
from fastapi import APIRouter
from app.schemas.category import CategoryCreateSchema, CategoryResponse, CategoryUpdateSchema

router = APIRouter(tags=["Categories"])

@router.get("/categories")
def get_categories(
    category_service: CategoryServiceDep
):
    return category_service.get_categories()

@router.get("/categories/{category_id}")
def get_category(category_id: int, category_service: CategoryServiceDep):
    return category_service.get_category(category_id)

@router.post("/categories")
def add_category(
    current_user: Current_user,
    creating_category: CategoryCreateSchema,
    category_service: CategoryServiceDep

): 
    return category_service.add_category(current_user=current_user, creating_category=creating_category)

@router.patch("/categories/{category_id}")
def change_category(
    category_id: int,
    category_service: CategoryServiceDep,
    current_user: Current_user,
    new_category: CategoryUpdateSchema

):
    return category_service.change_category(
        current_user=current_user,
        category_id=category_id,
        new_category=new_category
        )

@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    current_user: Current_user,
    category_service: CategoryServiceDep
):
    return category_service.delete_category(category_id, current_user)