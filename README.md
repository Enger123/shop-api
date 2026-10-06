# Shop API

REST API for online store using Python and FastAPI.

## Features

- User registration and authentication
- JWT authentication
- User roles (ADMIN, USER)
- Product management
- Category management
- Shopping cart
- Orders
- Product reviews
- Product stock management
- Redis caching
- PostgreSQL database
- Database migrations with Alembic
- API tests with pytest
- Docker and Docker Compose

## Tech stack

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Redis
- Pydantic
- JWT
- pytest
- Docker
- Docker Compose

## Project structure

```shop-api/
│   .gitignore
│   alembic.ini
│   docker-compose.yml
│   Dockerfile
│   main.py
│   pyproject.toml
│   README.md
│   requirements.txt              
│
├───app
│   ├───api
│   │   │   dependencies.py
│   │   │
│   │   ├───routers
│   │           auth.py
│   │           cart.py
│   │           category.py
│   │           order.py
│   │           product.py
│   │           review.py
│   │           user.py       
│   │
│   ├───cache
│   │    redis.py
│   │
│   ├───core
│   │      config.py
│   │      security.py
│   │   
│   │
│   ├───db
│   │      session.py
│   │
│   ├───models
│   │      base.py
│   │      cart.py
│   │      cart_item.py
│   │      category.py
│   │      order.py
│   │      order_item.py
│   │      product.py
│   │      review.py
│   │      user.py
│   │      __init__.py
│   │   
│   ├───repositories
│   │      cart.py
│   │      category.py
│   │      order.py
│   │      product.py
│   │      review.py
│   │      user.py
│   │   
│   ├───schemas
│   │      cart.py
│   │      category.py
│   │      order.py
│   │      product.py
│   │      review.py
│   │      user.py
│   │
│   └───services
│       │   cart.py
│       │   category.py
│       │   order.py
│       │   product.py
│       │   review.py
│       │   user.py
│       │   __init__.py
│
├───tests
│   │   conftest.py
│   │   database.py
│   │   test_auth.py
│   │   test_cache.py
│   │   test_carts.py
│   │   test_categories.py
│   │   test_orders.py
│   │   test_products.py
│   │   test_reviews.py
│   │   test_user.py
```

## Main functionality

### Authentication

Users can register and authenticate using JWT tokens.

The API supports two roles:
- USER
- ADMIN

Some operations, such as creating, updating and deleting products or categories are available only to administrators.

### Products

Admins can: 

- create products
- update products
- delete products

Products contain information such as:

- name
- description
- price
- stock
- category
- active status

### Shopping Cart

Authenticated users can add products to their cart.

The API checks whether the requested quantity is available in stock.

### Orders

Users can create an order from their shopping cart.

When an order is created:

1. Cart items are converted into order items.
2. The total order price is calculated.
3. Product stock is decreased.
4. Cart items are removed.

### Reviews

Users who have purchased a product can leave a review with a rating and text.

### Redis Cache

Redis is used to cache frequently requested data, such as products and categories.

The cache is invalidated when the corresponding data is created, updated or deleted.

### Running with Docker

Clone the repository:

**git clone https://github.com/Enger123/shop-api.git****
**cd shop-api**

Create a *.env* file with the required environment variables.

Then run:

__docker compose up --build__

The API will be available at:

**http://localhost:8000**

Interactive API documentation:

**http://localhost:8000/docs**

### Database Migrations

Run migrations inside the backend container:

**docker compose exec backend alembic upgrade head**

### Running Tests

Run:

**pytest**

The tests cover authentication, users, categories, products, shopping cart, orders and reviews.

## API Documentation

After starting the application, Swagger UI is available at:

**http://localhost:8000/docs**

ReDoc:

**http://localhost:8000/redoc**

