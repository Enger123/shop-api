from app.api.routers.user import router as users_router
from app.api.routers.auth import router as auth_router
from app.api.routers.product import router as product_router
from app.api.routers.category import router as category_router
from app.api.routers.order import router as order_router
from app.api.routers.cart import router as cart_router
from app.api.routers.review import router as review_router
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.messaging.rabbitmq import connect_rabbitmq, declare_orders_exchange, declare_notifications_queue
from app.messaging.consumer import start_notifications_consume

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Помилка до connect")
    connection = await connect_rabbitmq()
    print("Помилка до Try")

    try:
        channel = await connection.channel()

        app.state.order_exchange = await declare_orders_exchange(channel)

        await start_notifications_consume(connection=connection)

        yield
        
    finally:
        await connection.close()

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(order_router)
app.include_router(cart_router)
app.include_router(review_router)


