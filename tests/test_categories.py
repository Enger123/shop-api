from fastapi.testclient import TestClient

def test_add_category_admin(test_client: TestClient, token):
    response = test_client.post("/categories",
                                json={
                                    'name': 'Clothes'
                                },
                                headers={
                                    'Authorization': f'Bearer {token}'
                                }
                                )
    assert response.status_code == 200
    assert "Clothes" in response.json()['name']

def test_add_category_user(test_client: TestClient, token2):
    response = test_client.post("/categories",
                                json={
                                    'name': 'Clothes'
                                },
                                headers={
                                    'Authorization': f'Bearer {token2}'
                                }
                                )
    assert response.status_code == 403

def test_add_existing_category(test_client: TestClient, token, test_category):
    response = test_client.post("/categories",
                                json={
                                    'name': 'Clothes'
                                },
                                headers={
                                    'Authorization': f'Bearer {token}'
                                }
                                )
    assert response.status_code == 409

def test_get_categories(test_client: TestClient, test_category):
    response = test_client.get("/categories")
    data = response.json()
    assert response.status_code == 200
    assert 'Clothes' in data[0]['name']

def test_get_category(test_client: TestClient, test_category):
    response = test_client.get(f"/categories/9999")
    assert response.status_code == 200

def test_change_category_user(test_client: TestClient, test_category, token2):
    response = test_client.patch(f"/categories/{test_category['id']}",
                                 json={
                                     'name': 'Clothes2'
                                 },
                                 headers={
                                     'Authorization': f"Bearer {token2}"
                                 }
                                 )
    assert response.status_code == 403

def test_change_category_admin(test_client: TestClient, test_category, token):
    response = test_client.patch(f"/categories/{test_category['id']}",
                                 json={
                                     'name': 'Clothes2'
                                 },
                                 headers={
                                     'Authorization': f"Bearer {token}"
                                 }
                                 )
    assert response.status_code == 200
    assert response.json()['name'] == 'Clothes2'

def test_change_unexisting_category(test_client: TestClient, token):
    response = test_client.patch("/categories/9999",
                                 json={
                                     'name': 'Clothes2'
                                 },
                                 headers={
                                     'Authorization': f"Bearer {token}"
                                 }
                                 )
    assert response.status_code == 404

def test_delete_category_user(test_client: TestClient, test_category, token2):
    response = test_client.delete(f"/categories/{test_category['id']}",
                                 headers={
                                     'Authorization': f"Bearer {token2}"
                                 }
                                 )
    assert response.status_code == 403

def test_delete_category_admin(test_client: TestClient, test_category, token):
    response = test_client.delete(f"/categories/{test_category['id']}",
                                 headers={
                                     'Authorization': f"Bearer {token}"
                                 }
                                 )
    assert response.status_code == 200

def test_delete_unexisting_category(test_client: TestClient, token):
    response = test_client.delete(f"/categories/9999",
                                 headers={
                                     'Authorization': f'Bearer {token}'
                                 }
    )
    assert response.status_code == 404


