from fastapi.testclient import TestClient
import pytest

def test_get_products(test_client: TestClient):
    response = test_client.get("/products")
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_product_with_positive_stock(
    test_client: TestClient, 
    test_category,
    token
    ):
    response = test_client.post(f"/products/{test_category['id']}",
                               json={
                                   'name': 'Jeans',
                                   'description': 'Blue',
                                   'price': 8000,
                                   'stock': 2
                               },
                               headers={
                                   'Authorization': f"Bearer {token}"
                               }
                               )
    assert response.status_code == 200

def test_add_product_with_zero_stock(
    test_client: TestClient, 
    test_category,
    token
    ):
    response = test_client.post(f"/products/{test_category['id']}",
                               json={
                                   'name': 'Jeans',
                                   'description': 'Blue',
                                   'price': 8000,
                                   'stock': 0
                               },
                               headers={
                                   'Authorization': f'Bearer {token}'
                               }
                               )
    assert response.status_code == 422

def test_add_product_with_negative_stock(
    test_client: TestClient, 
    test_category,
    token
    ):
    response = test_client.post(f"/products/{test_category['id']}",
                               json={
                                   'name': 'Jeans',
                                   'description': 'Blue',
                                   'price': 8000,
                                   'stock': -1
                               },
                               headers={
                                   'Authorization': f'Bearer {token}'
                               }
                               )
    assert response.status_code == 422


@pytest.mark.parametrize(
    argnames='payload, exp_name, exp_desc, exp_price, exp_stock, exp_is_active',
    argvalues=[
        [{'name': 'Jeans'}, 'Jeans', 'Круті', 8000, 8, True],
        [{'name': 'Jeans', 'description': 'Круті', 'price': 2222, 'stock': 5, 'is_active': False}, 'Jeans', 'Круті', 2222, 5, False]
    ]
)
def test_change_products(
        payload,
        exp_name,
        exp_desc,
        exp_price,
        exp_stock,
        exp_is_active,
        test_product,
        token,
        test_client: TestClient
):
    response = test_client.patch(f"/products/{test_product['id']}",
                                 json=payload,
                                 headers={
                                     'Authorization': f"Bearer {token}"
                                 }
                                 )
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == exp_name
    assert data['description'] == exp_desc
    assert data['price'] == exp_price
    assert data['stock'] == exp_stock
    assert data['is_active'] == exp_is_active
