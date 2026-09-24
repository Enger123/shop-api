from app.api.dependencies import CartServiceDep, Current_user
from fastapi import APIRouter
from app.schemas.cart import CartSchema

router = APIRouter(tags=["Carts"])

@router.post("/carts-add-product")
def add_product_in_cart(
    creating_cart: CartSchema,
    current_user: Current_user,
    cart_service: CartServiceDep
):
    return cart_service.add_product_in_cart(creating_cart, current_user)
    
