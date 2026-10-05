import pytest
from fastapi.testclient import TestClient

def test_get_users(test_client: TestClient, test_user):
    response = test_client.get("/users")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert "aid@gmail.com" in data[0]['email']
    assert "ADMIN" in data[0]['role']

@pytest.mark.parametrize(
        argnames='payload, exp_status_code',
        argvalues=[
        [{'email': 'aid@gmail.com', 'password': '123123', 'role': 'ADMIN'}, 200],
        [{'email': 'aid@gmail.com', 'password': '12312', 'role': 'ADMIN'}, 422],
        [{'email': 'aid@gmail.com', 'password': '123123', 'role': 'MODERATOR'}, 422],
        [{'email': 'aid@gmail.com', 'password': '123123212222222222222222222222222222222222222222', 'role': 'ADMIN'}, 422]
        ]
)
def test_add_user(
    test_client: TestClient,
    payload,
    exp_status_code
    ):
    response = test_client.post("/users",
                                json=payload
                                )
    assert response.status_code == exp_status_code

def test_create_same_user(test_client: TestClient, test_user):
    response = test_client.post("/users",
                                    json={
                                    'email': 'aid@gmail.com',
                                    'password': '123123',
                                    'role': 'ADMIN'

                                }
                                )
    assert response.status_code == 403

def test_get_user(test_client: TestClient, test_user):
    response = test_client.get(f"/users/{test_user['id']}")

    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data['email'] == "aid@gmail.com"
    assert data['role'] == 'ADMIN'

def test_unexisting_user(test_client: TestClient):
    response = test_client.get("/users/9999")
    assert response.status_code == 404


@pytest.mark.parametrize(
    argnames='payload, exp_status_code',
    argvalues=[
        [{'email': 'asdad@fasf.caf'}, 200],
        [{'role': "USER"}, 200],
        [{'role': 'MODERATOR'}, 422],
        [{'email': 123}, 422]
    ]
)
def test_change_user(
    test_client: TestClient,
    token,
    test_user,
    payload,
    exp_status_code
):
    response = test_client.patch("/users",
                                 json=payload,
                                 headers={
                                     'Authorization': f"Bearer {token}"
                                 }
                                 )
    assert response.status_code == exp_status_code

def test_change_user_with_existing_user(
        test_client: TestClient,
        test_user
):
    response = test_client.patch("/users",
                                 json={
                                     'email': 'aid@gmail.com',
                                     'role': 'ADMIN'
                                 }
                                 )
    assert response.status_code == 401

def test_del_user(
        test_client: TestClient,
        token
):
    response = test_client.delete("/users", headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 200
    response = test_client.delete("/users", headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 401
