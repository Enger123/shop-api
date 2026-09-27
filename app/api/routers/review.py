from app.api.dependencies import ReviewServiceDep, Current_user
from fastapi import APIRouter
from app.schemas.review import ReviewCreateSchema

router = APIRouter(tags=['Reviews'])

@router.post("/reviews")
def create_review(
    current_user: Current_user,
    creating_review: ReviewCreateSchema,
    review_service: ReviewServiceDep
):
    return review_service.create_review(current_user, creating_review)

@router.get("/reviews/{product_id}")
def get_reviews_for_product(
    product_id: int,
    review_service: ReviewServiceDep
):
    return review_service.get_all_product_reviews(product_id)
