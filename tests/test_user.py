

def test_get_users(test_client, test_user):
    response = test_client.get("/users")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert "aid@gmail.com" in data[0]['email']

def test_add_user(test_client):
    response = test_client.post("/users",
                                json={
                                    'email': 'aid@gmail.com',
                                    'password': '123123',
                                    'role': 'ADMIN'

                                }
                                )
    data = response.json()
    print(data)
    assert 'aid@gmail.com' in data['email']