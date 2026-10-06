from fastapi.testclient import TestClient
import pytest

def test_login_success(test_client: TestClient, test_user, token):
    response = test_client.post("/token",
                                data={
                                    'username': 'aid@gmail.com',
                                    'password': '123123'
                                }
                                
                                )
    assert response.status_code == 200

@pytest.mark.parametrize(
        argnames='payload, exp_exc',
        argvalues=[
            [{'username': 'ai@gmail.com', 'password': '123123'}, 401],
            [{'username': 'aid@gmail.com', 'password': '123124'}, 401],
        ]
)
def test_login_with_invalid_username(
    test_client: TestClient, 
    test_user, 
    payload,
    exp_exc
    ):
    response = test_client.post("/token", data=payload)
    assert response.status_code == exp_exc