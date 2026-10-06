from fastapi.testclient import TestClient
import pytest

# def test_create_review(test_client: TestClient, test_product, token, test_order):
#     response = test_client.post(f"/products/{test_product['id']}/reviews",
#                                 json={
#                                     'rating': 5,
#                                     'text': 'Some text'
#                                 },
#                                 headers={
#                                     'Authorization': f"Bearer {token}"
#                                 }
#                                 )
#     data = response.json()
#     assert response.status_code == 200
#     assert data['rating'] == 5
#     assert data['text'] == 'Some text'

# def test_create_review_rating_more_ten(test_client: TestClient, test_product, token, test_order):
#     response = test_client.post(f"/products/{test_product['id']}/reviews",
#                                 json={
#                                     'rating': 11,
#                                     'text': 'Some text'
#                                 },
#                                 headers={
#                                     'Authorization': f"Bearer {token}"
#                                 }
#                                 )
#     assert response.status_code == 422

# def test_create_review_rating_less_zero(test_client: TestClient, test_product, token, test_order):
#     response = test_client.post(f"/products/{test_product['id']}/reviews",
#                                 json={
#                                     'rating': -1,
#                                     'text': 'Some text'
#                                 },
#                                 headers={
#                                     'Authorization': f"Bearer {token}"
#                                 }
#                                 )
#     assert response.status_code == 422


@pytest.mark.parametrize(
    argnames="payload, exp_status_code",
    argvalues=[
        [{"rating": 5, "text": "Some text"}, 200],
        [{"rating": -2, "text": "Some text"}, 422],
        [{"rating": 11, "text": "Some text"}, 422],
    ]
)
def test_create_review(
    test_client: TestClient,
    payload,
    exp_status_code,
    test_product,
    test_order,
    token
):
    response = test_client.post(
        f"/products/{test_product['id']}/reviews",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == exp_status_code


def test_create_review_unexisting_product(test_client: TestClient, token):
    response = test_client.post(f"/products/9999/reviews",
                                    json={
                                        'rating': 5,
                                        'text': 'Some text'
                                    },
                                    headers={
                                        'Authorization': f"Bearer {token}"
                                    }
                                    )
    assert response.status_code == 404

def test_create_review_not_ordering_product(
        test_client: TestClient,
        token,
        test_product
):
    response = test_client.post(f"/products/{test_product['id']}/reviews",
                                json={
                                    'rating': 5,
                                    'text': 'Some text'
                                },
                                headers={
                                    'Authorization': f"Bearer {token}"
                                })
    assert response.status_code == 404



def test_get_reviews_empty_list(test_client: TestClient, test_product):
    response = test_client.get(f"/reviews/{test_product['id']}")

    assert response.status_code == 200
    assert response.json() == []

def test_get_reviews_with_data(test_client: TestClient, test_product, test_review):
    response = test_client.get(f"/reviews/{test_product['id']}")

    data = response.json()
    assert response.status_code == 200
    assert data[0]['rating'] == 5
    assert data[0]['text'] == 'Some text'

