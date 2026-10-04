from fastapi.testclient import TestClient

def test_get_products_in_cart(test_client: TestClient, test_cart, token):
    response = test_client.get("/carts-get",
                                headers={
                                    'Authorization': f'Bearer {token}'
                                }
    )
    print(response.json())

    assert response.status_code == 200

def test_create_cart_success(test_client: TestClient, test_product, token):
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

def test_create_cart_with_notfound_product(test_client: TestClient, test_product, token):
    response = test_client.post("/carts-add-product",
                                json={
                                    'product_id': 2,
                                    'quantity': 1 
                                },
                                headers={
                                    'Authorization': f'Bearer {token}'
                                }
                                )
    assert response.status_code == 404

def test_create_cart_with_notenouh_stock(test_client: TestClient, token, test_product):
    response = test_client.post("/carts-add-product",
                                    json={
                                        'product_id': 1,
                                        'quantity': 9
                                    },
                                    headers={
                                        'Authorization': f'Bearer {token}'
                                    }
                                    )
    assert response.status_code == 409