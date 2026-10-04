from fastapi.testclient import TestClient

def test_add_category(test_client: TestClient, token):
    response = test_client.post("/categories",
                                json={
                                    'name': 'Electro'
                                },
                                headers={
                                    'Authorization': f'Bearer {token}'
                                }
                                )
    assert response.status_code == 200
    assert "Electro" in response.json()['name']

def test_get_categories(test_client: TestClient, test_category):
    response = test_client.get("/categories")
    data = response.json()
    assert response.status_code == 200
    assert 'Clothes' in data[0]['name']