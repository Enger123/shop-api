from fastapi.testclient import TestClient
import pytest
from main import app
from app.models.base import Base
from tests.database import test_db
from sqlalchemy import text

@pytest.fixture
def test_client():
    with TestClient(app=app) as client:
        yield client

@pytest.fixture(scope='session', autouse=True)
def create_tables():
    Base.metadata.create_all(bind=test_db)
    yield
    Base.metadata.drop_all(bind=test_db)

@pytest.fixture(autouse=True)
def clean_db():
    yield

    with test_db.begin() as conn:
        conn.execute(text("""TRUNCATE TABLE
        users,  
        categories, 
        products,
        carts,
        cart_items,
        orders,
        order_items,
        reviews RESTART IDENTITY CASCADE"""
        ))

@pytest.fixture
def test_user(test_client: TestClient):
    response = test_client.post("/users",
                                    json={
                                        'email': 'aid@gmail.com',
                                        'password': '123123',
                                        'role': 'ADMIN'
    
                                    }
                                    )
    data = response.json()
    assert response.status_code == 200
    assert 'aid@gmail.com' in data['email']
    return data

@pytest.fixture
def token(test_client: TestClient, test_user):
    login = test_client.post("/token",
                                data={
                                    'username': test_user['email'],
                                    'password': '123123'
                                }
                                )
    assert login.status_code == 200
    return login.json()['access_token']

@pytest.fixture
def test_category(test_client: TestClient, token):
    response = test_client.post("/categories",
                                        json={
                                            'name': 'Clothes',
                                        },
                                        headers={
                                            'Authorization': f'Bearer {token}'
                                        }
                                        )
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def test_product(test_client: TestClient, test_category, token):
    response = test_client.post(f"/products/{test_category['id']}",
                                json={
                                    'name': 'Штани',
                                    'description': 'Круті',
                                    'price': 8000,
                                    'stock': 8,
                                    'category_id': test_category['id'],
                                    'is_active': True
                                },
                                headers={
                                    'Authorization': f'Bearer {token}'
                                }
                                        )
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def test_cart(test_client: TestClient, test_product, token):
    response = test_client.post("/carts-add-product",
                                json={
                                    'product_id': test_product['id'],
                                    'quantity': 3
                                },
                                headers={
                                    'Authorization': f'Bearer {token}'
                                }
                                
                                )
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def test_order(test_client: TestClient, test_cart, token):
    response = test_client.post("/orders",
                                headers={
                                    'Authorization': f'Bearer {token}'
                                }
                                )
    assert response.status_code == 200
    return response.json()





