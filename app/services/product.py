from sqlalchemy.orm import Session
from app.repositories.product import ProductRepository
from fastapi import HTTPException
from app.schemas.product import ProductResponse, ProductCreateSchema, ProductUpdateSchema

class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.product_repository = ProductRepository(db)

    def get_product(self, product_id: int):
        product = self.product_repository.get_product(product_id)
        if not product:
            raise HTTPException(status=404, detail='Product not found')
        return ProductResponse.model_validate(product)

    def get_products(self):
        products = self.product_repository.get_products()
        return [ProductResponse.model_validate(product) 
                for product in products]

    def create_product(
                self,
                current_user,
                creating_product: ProductCreateSchema
                ):
        if current_user.role != 'ADMIN':
            raise HTTPException(status_code=403, detail="User can't add product")
        product = self.product_repository.add_product(creating_product)
        self.db.commit()
        self.db.refresh(product)
        return ProductResponse.model_validate(product)

    def change_product(
                self,
                current_user,
                product_id: int,
                new_product: ProductUpdateSchema
                ):
        if current_user.role != 'ADMIN':
            raise HTTPException(status_code=403, detail="User can't change product")
        product = self.product_repository.get_product_with_userid(product_id, current_user.id)
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
        return ProductResponse.model_validate(product)

    def delete_product(
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
    
          
        