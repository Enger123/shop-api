from app.api.dependencies import ReviewServiceDep, Current_user
from fastapi import APIRouter
from app.schemas.review import ReviewCreateSchema

router = APIRouter(tags=['Reviews'])

@router.post("/products/{product_id}/reviews")
def create_review(
    product_id: int,
    current_user: Current_user,
    creating_review: ReviewCreateSchema,
    review_service: ReviewServiceDep
):
    return review_service.create_review(product_id, current_user, creating_review)

@router.get("/reviews/{product_id}")
def get_reviews_for_product(
    product_id: int,
    review_service: ReviewServiceDep
):
    return review_service.get_all_product_reviews(product_id)
