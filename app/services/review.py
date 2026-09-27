from sqlalchemy.orm import Session
from app.models.review import Review
from app.models.product import Product
from app.schemas.review import ReviewCreateSchema, ReviewResponse
from sqlalchemy import select
from app.repositories.review import ReviewRepository
from app.repositories.order import OrderRepository
from fastapi import HTTPException

class ReviewService:
    def __init__(self, db: Session):
        self.db = db
        self.review_repository = ReviewRepository(db)
        self.order_repository = OrderRepository(db)

    #вибє помилка коли додати product_id не існуючий
    def create_review(self, current_user, creating_review: ReviewCreateSchema):
        user_order = self.order_repository.get_my_order(
            current_user.id, creating_review.order_id)
        if not user_order:
            raise HTTPException(status_code=404, detail='User did not order this item')

        review = self.review_repository.create_review(
            current_user.id, creating_review
        )
        self.db.commit()
        self.db.refresh(review)
        return ReviewResponse.model_validate(review)

    def get_all_product_reviews(self, product_id):
        reviews = self.review_repository.list_reviews_for_product(product_id)
        return [
            ReviewResponse.model_validate(review) for review in reviews
        ]
            
