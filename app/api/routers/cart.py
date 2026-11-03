from app.api.dependencies import CartServiceDep, Current_user
from fastapi import APIRouter
from app.schemas.cart import CartSchema, CartResponse

router = APIRouter(tags=["Carts"])

@router.post("/carts-add-product", response_model=CartResponse)
def add_product_in_cart(
    creating_cart: CartSchema,
    current_user: Current_user,
    cart_service: CartServiceDep
):
    return cart_service.add_product_in_cart(creating_cart, current_user)
    
@router.get("/carts-get", response_model=list[CartResponse])
def get_from_cart(
    current_user: Current_user,
    cart_service: CartServiceDep
    ):
    return cart_service.get_products_in_my_cart(current_user)
