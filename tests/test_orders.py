from fastapi.testclient import TestClient

def test_add_products_to_orders(
        test_client: TestClient, 
        test_product, 
        test_cart, 
        token
        ):
    headers={'Authorization': f'Bearer {token}'}
    response = test_client.post("/orders", headers=headers)

    assert response.status_code == 200

    response2 = test_client.get(f"/products/{test_product['id']}")
    data = response2.json()
    
    assert response2.status_code == 200
    assert data['stock'] == 5

def test_get_my_orders(test_client: TestClient, token, test_order):
    response = test_client.get("/my-orders",
                                headers={
                                    'Authorization': f'Bearer {token}'
                                }
                                    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_my_order(test_client: TestClient, token, test_order):
    response = test_client.get(f"/my-order/{test_order['id']}",
                                headers={
                                    'Authorization': f'Bearer {token}'
                                }
                                    )
    print(response.json())
    assert response.status_code == 200

def test_add_to_orders_notfound_cart(test_client: TestClient, token):
    response = test_client.post(f"/orders",
                                    headers={
                                        'Authorization': f'Bearer {token}'
                                    }
                                        )
    assert response.status_code == 404