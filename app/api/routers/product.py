from app.api.dependencies import ProductServiceDep, Current_user
from fastapi import APIRouter
from app.schemas.product import ProductResponse, ProductUpdateSchema, ProductCreateSchema

router = APIRouter(tags=["Products"])

@router.get("/products")
def list_products(product_service: ProductServiceDep):
    return product_service.get_products()

@router.get("/products/{id}")
def get_product(product_id: int, product_service: ProductServiceDep):
    return product_service.get_product(product_id)

@router.post("/products/{category_id}")
def create_product(
    category_id: int,
    current_user: Current_user, 
    new_product: ProductCreateSchema,
    product_service: ProductServiceDep
                   ):
    return product_service.create_product(category_id, current_user, new_product)

@router.patch("/products/{product_id}")
def change_product(
    current_user: Current_user,
    product_id: int,
    new_product: ProductUpdateSchema,
    product_service: ProductServiceDep
):
    return product_service.change_product(current_user, product_id, new_product)

@router.delete("/products/{product_id}")
def delete_product(
    current_user: Current_user,
    product_id: int,
    product_service: ProductServiceDep
):
    return product_service.delete_product(
        product_id=product_id, current_user=current_user)