from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryResponse, CategoryCreateSchema, CategoryUpdateSchema
from app.cache.redis import RedisCachedBackend
from app.core.config import settings

class CategoryService:

    CACHE_CATEGORIES_KEY = "cache:categories"
    
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)
        self.cache = RedisCachedBackend(redis_url=settings.REDIS_URL, cache_ttl_seconds=settings.CACHE_TTL_SECONDS)

    def get_current_admin(self, current_user, operation: str):
        if current_user.role != 'ADMIN':
            raise HTTPException(status_code=403, detail=f"User can't {operation} categories")
    
    def get_categories(self):
        cache = self.cache.list_cache(self.CACHE_CATEGORIES_KEY)
        if cache is not None:
            return [CategoryResponse.model_validate(category) 
                for category in cache]
        
        categories = self.category_repository.get_categories()

        categories_to_return = [CategoryResponse.model_validate(category) 
                for category in categories]
        
        data_for_cache = [category.model_dump(mode='json') for category in categories_to_return]

        self.cache.set_cache(self.CACHE_CATEGORIES_KEY, data_for_cache)

        return categories_to_return

    def add_category(
                self,
                current_user,
                creating_category: CategoryCreateSchema
                ):
        self.get_current_admin(current_user, "create")

        category = self.category_repository.get_category_by_name(creating_category.name)
        if category is not None:
            raise HTTPException(status_code=409, detail='Category exists')
        
        new_category = self.category_repository.add_category(creating_category)
        self.db.commit()
        self.db.refresh(new_category)
        self.cache.delete_cache(self.CACHE_CATEGORIES_KEY)
        return CategoryResponse.model_validate(new_category)

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
        self.cache.delete_cache(self.CACHE_CATEGORIES_KEY)
        return CategoryResponse.model_validate(category)

    def delete_category(
                self, 
                category_id: int, 
                current_user
                ):
          self.get_current_admin(current_user, "delete")

          category = self.category_repository.get_category(category_id)
          if not category:
            raise HTTPException(status_code=404, detail='Category not found')
          
          self.category_repository.delete_category(category)
          self.db.commit()
          self.cache.delete_cache(self.CACHE_CATEGORIES_KEY)
          return {'message': 'Category deleted'}
    
          
        