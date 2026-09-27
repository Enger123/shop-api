from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Category
from app.schemas.category import CategoryCreateSchema, CategoryResponse, CategoryUpdateSchema

class CategoryRepository:
    def __init__(self, db: Session):
            self.db = db
    
    def get_categories(self):
            return self.db.scalars(select(Category)).all()
    
    def get_category(self, category_id: int):
            return self.db.scalars(select(Category)
                  .where(Category.id==category_id)).first()

    def get_category_by_name(self, name: str):
           return self.db.scalars(select(Category)
                        .where(Category.name==name)).first()
    
    
    def add_category(self, creating_category: CategoryCreateSchema):
            new_category = Category(
                name=creating_category.name
            )
            self.db.add(new_category)
            return new_category
    
    def delete_category(self, category):
            self.db.delete(category)