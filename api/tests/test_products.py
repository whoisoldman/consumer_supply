# api/tests/test_products.py
import pytest
from rest_framework import status

@pytest.mark.django_db
def test_create_product(api_client, supplier_token):
    url = "/api/products/"
    data = {
        "name": "Product E",
        "description": "Description of Product E",
        "price": "49.99"
    }
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {supplier_token}")
    response = api_client.post(url, data, format="json")
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Product creation failed: {response.content}"
    assert response.data["name"] == "Product E"
    assert response.data["price"] == "49.99"
    assert "id" in response.data, "Product creation response does not contain 'id'"
