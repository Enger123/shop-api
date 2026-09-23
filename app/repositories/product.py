from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Product
from app.schemas.product import ProductCreateSchema, ProductResponse, ProductUpdateSchema

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_products(self):
        return self.db.scalars(select(Product)).all()

    def get_product(self, product_id: int):
        return self.db.scalars(select(Product)
              .where(Product.id==product_id)).first()

    def get_product_with_userid(self, product_id: int, user_id: int):
            return self.db.scalars(select(Product)
                  .where(Product.id==product_id,
                         Product.user_id==user_id)
                  ).first()

    def add_product(self, creating_product: ProductCreateSchema):
        new_product = Product(
            name=creating_product.name,
            description=creating_product.description,
            price=creating_product.price,
            stock=creating_product.stock
        )
        self.db.add(new_product)
        return new_product

    def delete_product(self, product):
        self.db.delete(product)


    