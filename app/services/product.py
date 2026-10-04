from sqlalchemy.orm import Session
from app.repositories.product import ProductRepository
from app.repositories.category import CategoryRepository
from fastapi import HTTPException
from app.schemas.product import ProductResponse, ProductCreateSchema, ProductUpdateSchema
from app.cache.redis import RedisCachedBackend
from app.core.config import settings

class ProductService:

    CACHE_PRODUCTS_KEY="cache:products"

    def __init__(self, db: Session):
        self.db = db
        self.cache = RedisCachedBackend(settings.REDIS_URL, settings.CACHE_TTL_SECONDS)
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_current_admin(self, current_user, operation: str):
        if current_user.role != 'ADMIN':
            raise HTTPException(status_code=403, detail=f"User can't {operation} product")

    def get_product(self, product_id: int):
        product = self.product_repository.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Product not found')
        return ProductResponse.model_validate(product)

    def get_products(self):
        cache_data = self.cache.list_cache(self.CACHE_PRODUCTS_KEY) 
        if cache_data is not None:
             return [ProductResponse.model_validate(product) 
                for product in cache_data]
        
        products = self.product_repository.get_products()

        products_to_return = [ProductResponse.model_validate(product) 
                for product in products]
        
        data_in_cache = [product.model_dump(mode="json") for product in products_to_return]
        
        self.cache.set_cache(self.CACHE_PRODUCTS_KEY, data_in_cache)

        return products_to_return

    def create_product(
                self,
                category_id: int,
                current_user,
                creating_product: ProductCreateSchema
                ):
        self.get_current_admin(current_user, "create")

        category = self.category_repository.get_category(category_id)
        if not category:
             raise HTTPException(status_code=404, detail='Category not found')
        
        product = self.product_repository.add_product(category_id, creating_product)
        self.db.commit()
        self.db.refresh(product)
        self.cache.delete_cache(self.CACHE_PRODUCTS_KEY)
        return ProductResponse.model_validate(product)

    def change_product(
                self,
                current_user,
                product_id: int,
                new_product: ProductUpdateSchema
                ):
        self.get_current_admin(current_user, "update")

        product = self.product_repository.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Product not found')
        
        if new_product.name is not None:
            product.name = new_product.name
        if new_product.description is not None:
                    product.description = new_product.description
        if new_product.stock is not None:
                    product.stock = new_product.stock
        if new_product.price is not None:
                    product.price = new_product.price
        if new_product.is_active is not None:
            product.is_active = new_product.is_active   
        self.db.commit()
        self.db.refresh(product)
        self.cache.delete_cache(self.CACHE_PRODUCTS_KEY)
        return ProductResponse.model_validate(product)

    def delete_product(
                self, 
                product_id: int, 
                current_user
                ):
          self.get_current_admin(current_user, "delete")

          product = self.product_repository.get_product(product_id)
          if not product:
            raise HTTPException(status_code=404, detail='Product not found')
          
          self.product_repository.delete_product(product)
          self.db.commit()
          self.cache.delete_cache(self.CACHE_PRODUCTS_KEY)
          return {'message': 'Product deleted'}
    
          
        