from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryResponse, CategoryCreateSchema, CategoryUpdateSchema

class CategoryService:
    
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def get_category(self, category_id: int):
        category = self.category_repository_repository.get_category(category_id)
        if not category:
            raise HTTPException(status=404, detail='Product not found')
        return CategoryResponse.model_validate(category)

    def get_categories(self):
        categories = self.category_repository.get_products()
        return [CategoryResponse.model_validate(category) 
                for category in categories]

    def add_category(
                self,
                current_user,
                creating_category: CategoryCreateSchema
                ):
        if current_user.role != 'ADMIN':
            raise HTTPException(status_code=403, detail="User can't add product")
        category = self.product_repository.add_product(creating_category)
        self.db.commit()
        self.db.refresh(category)
        return CategoryResponse.model_validate(category)

    def change_category(
                self,
                current_user,
                category_id: int,
                new_category: CategoryUpdateSchema
                ):
        if current_user.role != 'ADMIN':
            raise HTTPException(status_code=403, detail="User can't change product")
        category = self.category_repository.get_product_with_userid(category_id, current_user.id)
        if not category:
            raise HTTPException(status_code=404, detail='Product not found')
        if new_category.name is not None:
            category.name = new_category.name 
        self.db.commit()
        self.db.refresh(category)
        return CategoryResponse.model_validate(category)

    def delete_category(
                self, 
                product_id: int, 
                current_user
                ):
          product = self.product_repository.get_product_with_userid(product_id, current_user.id)
          if current_user.role != 'ADMIN':
            raise HTTPException(status_code=403, detail="User can't delete product")
          if not product:
            raise HTTPException(status=404, detail='Product not found')
          self.product_repository.delete_product(product_id)
          self.db.commit()
          return {'message': 'Product deleted'}
    
          
        