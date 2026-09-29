from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreateSchema
from sqlalchemy import select

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_review(
            self,
            user_id: int, 
            order_id: int,
            product_id: int,
            rating: int,
            text: str
            ):
        new_review = Review(
            user_id=user_id,
            order_id=order_id,
            product_id=product_id,
            rating=rating,
            text=text
        )
        self.db.add(new_review)
        return new_review

    def list_reviews_for_product(self, product_id: int):
        return self.db.scalars(
            select(Review)
            .where(Review.product_id==product_id)
            ).all()

    
        