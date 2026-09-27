from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreateSchema
from sqlalchemy import select

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_review(self, user_id: int, creating_review: ReviewCreateSchema):
        new_review = Review(
            user_id=user_id,
            order_id=creating_review.order_id,
            product_id=creating_review.product_id,
            rating=creating_review.rating,
            text=creating_review.text
        )
        self.db.add(new_review)
        return new_review

    def list_reviews_for_product(self, product_id: int):
        return self.db.scalars(
            select(Review)
            .where(Review.product_id==product_id)
            ).all()

    
        