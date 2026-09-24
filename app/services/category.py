from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryResponse, CategoryCreateSchema, CategoryUpdateSchema

class CategoryService:
    
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def get_current_admin(self, current_user, operation: str):
        if current_user.role != 'ADMIN':
            raise HTTPException(status_code=403, detail=f"User can't {operation} categories")
    
    def get_categories(self):
        categories = self.category_repository.get_categories()
        return [CategoryResponse.model_validate(category) 
                for category in categories]

    def add_category(
                self,
                current_user,
                creating_category: CategoryCreateSchema
                ):
        self.get_current_admin(current_user, "create")
        category = self.category_repository.add_category(creating_category)
        self.db.commit()
        self.db.refresh(category)
        return CategoryResponse.model_validate(category)

    def change_category(
                self,
                current_user,
                category_id: int,
                new_category: CategoryUpdateSchema
                ):
        self.get_current_admin(current_user, "update")
        category = self.category_repository.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail='Product not found')
        if new_category.name is not None:
            category.name = new_category.name 
        self.db.commit()
        self.db.refresh(category)
        return CategoryResponse.model_validate(category)

    def delete_category(
                self, 
                category_id: int, 
                current_user
                ):
          category = self.category_repository.get_category(category_id)
          self.get_current_admin(current_user, "delete")
          if not category:
            raise HTTPException(status=404, detail='Category not found')
          self.category_repository.delete_category(category)
          self.db.commit()
          return {'message': 'Category deleted'}
    
          
        