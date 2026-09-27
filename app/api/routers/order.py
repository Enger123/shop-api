from app.api.dependencies import Current_user, OrderServiceDep
from fastapi import APIRouter

router = APIRouter(tags=["Orders"])

@router.get("/my-orders")
def get_my_orders(
    current_user: Current_user,
    order_service: OrderServiceDep
):
    return order_service.get_my_orders(current_user)

@router.get("/my-order/{order_id}")
def get_my_order(
    order_id: int,
    current_user: Current_user,
    order_service: OrderServiceDep
):
    return order_service.get_my_order(order_id=order_id, current_user=current_user)

@router.post("/orders")
def add_products_in_order(
    current_user: Current_user,
    order_service: OrderServiceDep
):
    return order_service.add_to_orders(current_user)